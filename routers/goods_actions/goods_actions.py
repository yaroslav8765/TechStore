from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel, Field
from ...database import SessionLocal
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Annotated
from ...routers.auth import get_current_user
from starlette import status
from ...models import Goods, Basket, OrderItem, Orders, Users, Smartphones, Laptops
from ...routers.email_actions.email_verification import send_verification_email
from ...routers.auth import check_if_user_enter_email_or_phone_num
from ...routers.email_actions.email_mailing import send_order_details, send_cancel_order_notification

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

CATEGORY_TO_MODEL = {
    "laptops": Laptops,
    "smartphones": Smartphones
}

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

@router.get("/{category}/{goods_name}", status_code = status.HTTP_200_OK)
async def get_goods_info(db: db_dependancy, category: str, goods_name: str):
    model = CATEGORY_TO_MODEL.get(category.lower())

    goods_base_info = db.query(Goods).filter(func.lower(Goods.name) == goods_name.lower()).first()

    if model is None:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    goods_details_model = db.query(model).filter(model.goods_id == goods_base_info.id).first()

    if goods_details_model is None:
        raise HTTPException(status_code=404, detail="Goods not found")

    return goods_base_info, goods_details_model