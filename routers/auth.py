from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette import status
from pydantic import BaseModel, EmailStr, Field, field_validator
from models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError
from routers.email_verification import send_verification_email
from config import settings

import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

from email_validator import validate_email

utc_plus_2 = timezone(timedelta(hours=2))


router = APIRouter(
    prefix = "/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated = "auto") 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "auth/token")

class CreateUserRequest(BaseModel):
    #email: EmailStr  
    #phone_number: str = Field(min_length = 10, max_length = 13)  
    email_or_phone_number: str
    first_name: str = Field(min_length = 1, max_length = 50)      
    last_name: str = Field(min_length = 1, max_length = 50, default = None)            
    password: str      

    # @field_validator('phone_number')
    # def validate_phone_number(cls, value):
    #     try:
    #         parsed_number = parse(value, "UA") 
    #         if not is_valid_number(parsed_number):
    #             raise HTTPException(status_code=400, detail="Invalid phone number")
    #     except Exception:
    #         raise HTTPException(status_code=400, detail="Invalid phone number")
    #     return value




class Token(BaseModel):
    access_token: str
    token_type: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#По сути, мы тут создаём зависимость, которая будет возвращать объект сессии, который мы будем использовать в запросах к БД.
db_dependancy = Annotated[Session, Depends(get_db)]
#Это аннотация, которая говорит FastAPI, что это зависимость, которая возвращает объект сессии.

def authenticate_user(login: str, password: str, db: db_dependancy):
    user = db.query(Users).filter(or_(Users.email == login, Users.phone_number == login)).first()
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    if not bcrypt_context.verify(password, user.hashed_password): 
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "Wrong password")
    return user

def create_access_token(login: str, user_id:str, role:str, expires_delta: timedelta):
    encode = {"sub": login, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try: 
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Could not validate user")
        return {"username":username, "id":user_id, "role":user_role}
    except JWTError:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Could not validate user")


def check_if_user_enter_email_or_phone_num(login: str):
    try:
        if carrier._is_mobile(number_type(phonenumbers.parse(login))):
            return "Phone_number"
    except:
        try:
            email = validate_email(login)
            return "Email"
        except:
            return "Something wrong with your email or phone number. Please, check if your information is correct"

############END POINTS############
@router.post("/create-user", status_code= status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, new_user_request: CreateUserRequest):

    user_enter = check_if_user_enter_email_or_phone_num(new_user_request.email_or_phone_number)

    if(user_enter == "Email"):
        check_user = db.query(Users).filter((Users.email == new_user_request.email_or_phone_number)).first()

        if(check_user is not None):
            if check_user.is_active == False:
                await send_verification_email(new_user_request.email_or_phone_number)
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Please, verify your e-mail. We`ve sent you activation email again")
            else:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User witch such email already exists")
    
        await send_verification_email(new_user_request.email_or_phone_number)

        create_user_model = Users(
        email = new_user_request.email_or_phone_number,
        first_name = new_user_request.first_name,
        last_name = new_user_request.last_name,
        hashed_password = bcrypt_context.hash(new_user_request.password),
        role = "user",
        is_active = False
        )

        db.add(create_user_model)
        db.commit()


    elif(user_enter == "Phone_number"):
        check_user = db.query(Users).filter((Users.phone_number == new_user_request.email_or_phone_number)).first()
        if(check_user is not None):
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User witch such phone number already exists")
    
        #send verification SMS?)
        create_user_model = Users(
            phone_number = new_user_request.email_or_phone_number,
            first_name = new_user_request.first_name,
            last_name = new_user_request.last_name,
            hashed_password = bcrypt_context.hash(new_user_request.password),
            role = "user",
            is_active = False
        )
        db.add(create_user_model)
        db.commit()
    
    else:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User enter invalid phone number or password")
    


@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependancy):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,  detail = "Could not validate user")
    token = create_access_token(user.email, user.id, user.role, timedelta(minutes = 20))
    return {"access_token":token, "token_type":"bearer"}



