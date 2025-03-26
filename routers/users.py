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

class EditTheBasketRequest(BaseModel):
    goods_id: int            
    new_quantity: int



@router.get("/show-basket", status_code = status.HTTP_200_OK)
async def show_basket(db: db_dependancy, user: user_dependency):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    goods_to_return = []

    return db.query(Basket).filter(Basket.user_id == user.get("id")).all()




@router.post("/add-to-basket", status_code = status.HTTP_201_CREATED)
async def add_to_the_basket(db: db_dependancy, user: user_dependency, request: AddToTheBasketRequest):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    goods_info = db.query(Goods).filter(Goods.id == request.goods_id).first()
    if goods_info is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No goods with such ID")
    if goods_info.quantity < request.quantity:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"We don`t have enought goods. There is only {goods_info.quantity}")

    add_to_basket_model = Basket(
        goods_id = goods_info.id,
        user_id = user.get("id"),
        quantity = request.quantity,
        price_for_the_one = goods_info.price
    )
    db.add(add_to_basket_model)
    db.commit()
    
    

@router.put("/basket-edit",status_code = status.HTTP_202_ACCEPTED)
async def edit_basket(db: db_dependancy, user: user_dependency, request: EditTheBasketRequest ):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    edit_basket_model = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request.goods_id).first()
    if edit_basket_model is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No goods with such ID")
    #Короче сделать, если товар есть в корзине, то вместо добавления новой записи, чделать, чтобы оно добавляло в к старой
    edit_basket_model.quantity = request.new_quantity

    db.add(edit_basket_model)
    db.commit()



@router.delete("/basket-delete-good", status_code = status.HTTP_202_ACCEPTED)
async def delete_goods_from_basket(db: db_dependancy, user: user_dependency, goods_id: int):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    delete_model = db.query(Basket).filter(Basket.goods_id == goods_id).filter(Basket.user_id == user.get('id')).first()
    if delete_model is None:
        raise HTTPException(status_code=404, detail='Goods not found.')
    db.query(Basket).filter(Basket.goods_id == goods_id).filter(Basket.user_id == user.get('id')).delete()
    db.commit()







