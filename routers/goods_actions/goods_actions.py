from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from routers.auth import get_current_user
from starlette import status
from models import Goods, Basket, OrderItem, Orders, Users
from routers.email_actions.email_verification import send_verification_email
from routers.auth import check_if_user_enter_email_or_phone_num
from routers.email_actions.email_mailing import send_order_details, send_cancel_order_notification

router = APIRouter(
    prefix = "/goods",
    tags=["goods"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code = status.HTTP_200_OK)
async def show_goods_categories(db: db_dependancy):
    all_categories = db.query(Goods.category).distinct().all()
    return [category[0] for category in all_categories]

@router.get("/{category}", status_code = status.HTTP_200_OK)
async def show_category_goods(db: db_dependancy, category: str):
    category_goods = db.query(Goods).filter(Goods.category == category).all()
    if not category_goods:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No such category")
    return category_goods
