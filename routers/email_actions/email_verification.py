from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ...models import Users
from ...config import settings
from starlette import status

router = APIRouter(
    prefix = "/verify-email",
    tags=["verify-email"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy = Annotated[Session, Depends(get_db)]


def generate_verification_token(email: str):
    expires = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"sub": email, "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm= settings.ALGORITHM)

def decode_verification_token(token: str):
    try:
        payload = jwt.decode(token,  settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload["sub"]
    except jwt.JWTError:
        return None

conf = ConnectionConfig(
    MAIL_USERNAME="pechorkin2014@gmail.com",
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="pechorkin2014@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False  
)


async def send_verification_email(email: str):
    token = generate_verification_token(email)
    verification_url = f"http://127.0.0.1:8000/verify-email/?token={token}"

    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Click the link to verify your email: {verification_url}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

@router.get("/")
async def verify_email(token: str, db: db_dependancy):
    email = decode_verification_token(token)
    if not email:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    user.email = email
    db.commit()
    return {"message": "Email verified successfully!"}