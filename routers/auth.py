from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from starlette import status
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError
utc_plus_2 = timezone(timedelta(hours=2))
SECRET_KEY = "13f4493407503897508137ab8897987cd987987fdf897"
ALGORITHM = "HS256"


router = APIRouter(
    prefix = "/auth",
    tags=["auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated = "auto") 

class CreateUserRequest(BaseModel):
    email: str = Field(default = None) #add check email         
    phone_number: str = Field(min_length = 10, max_length = 13)  
    first_name: str = Field(min_length = 1, max_length = 50)      
    last_name: str = Field(min_length = 1, max_length = 50, default = None)            
    hashed_password: str      




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
    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)


############END POINTS############
@router.post("/create_user", status_code= status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, new_user_request: CreateUserRequest):
    check_user = db.query(Users).filter((Users.email == new_user_request.email)).first()
    if(check_user is not None):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User witch such email already exists")
    
    check_user = db.query(Users).filter((Users.phone_number == new_user_request.phone_number)).first()
    if(check_user is not None):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "User witch such phone number already exists")
    

    create_user_model = Users(
        email = new_user_request.email,
        phone_number = new_user_request.phone_number,
        first_name = new_user_request.first_name,
        last_name = new_user_request.last_name,
        hashed_password = bcrypt_context.hash(new_user_request.hashed_password),
        role = "user"
    )

    db.add(create_user_model)
    db.commit()


@router.get("/login", status_code= status.HTTP_200_OK)
async def get_access_token(login: str, password: str, db: db_dependancy):
    user = authenticate_user(login, password, db)
    if(user is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    token = create_access_token(login, user.id, user.role ,timedelta(days = 365))
    return {"access_token":token, "token_type":"bearer"}



