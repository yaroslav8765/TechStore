from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from routers.auth import get_current_user
from starlette import status
from models import Goods, Basket


router = APIRouter(
    prefix = "/user",
    tags=["/user"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class AddToTheBasketRequest(BaseModel):
    goods_id: int            
    quantity: int






    
@router.post("/add-to-basket", status_code = status.HTTP_201_CREATED)
async def add_to_the_basket(db: db_dependancy, user: user_dependency, request: AddToTheBasketRequest):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    goods_info = db.query(Goods).filter(Goods.id == request.goods_id).first()
    if goods_info is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No goods with such ID")
    add_to_basket_model = Basket(
        goods_id = goods_info.id,
        users_id = user.get("id"),
        quantity = AddToTheBasketRequest.quantity,
        price_for_the_one = goods_info.price
    )
    db.add(add_to_basket_model)
    db.commit()
    
    

















