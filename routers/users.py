from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel, Field
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from ..routers.auth import get_current_user
from starlette import status
from ..models import Goods, Basket, OrderItem, Orders, Users
from ..routers.email_actions.email_verification import send_verification_email
from ..routers.auth import check_if_user_enter_email_or_phone_num
from ..routers.email_actions.email_mailing import send_order_details, send_cancel_order_notification
from passlib.context import CryptContext

router = APIRouter(
    prefix = "/user",
    tags=["user"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"],deprecated = "auto") 

class AddToTheBasketRequest(BaseModel):
    goods_id: int            
    quantity: int = Field(gt = 0)

class EditTheBasketRequest(BaseModel):
    goods_id: int            
    new_quantity: int = Field(gt = 0)

class CreateOrderRequest(BaseModel):
    reciever_name: str = Field(min_length = 2, max_length = 30)
    shipping_adress: str = Field(min_length = 2, max_length = 100)

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "reciever_name" : "Tohru", 
                "shipping_adress" : "Miss Kobayashi's Home"
            }
        }
    }

class RecoverPasswordRequest(BaseModel):
    old_password: str
    new_password: str 

class EditUserRequest(BaseModel):
    first_name: str = Field(min_length = 2, max_length = 30)
    last_name: str = Field(min_length = 2, max_length = 50)
    phone_number: str 
    email: str

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "first_name" : "Empty", 
                "last_name" : "Empty",
                "phone_number" : "Empty",
                "email" : "Empty"
            }
        }
    }

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
    user_basket_info = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request.goods_id).first()
    if user_basket_info is not None:
        user_basket_info.quantity += request.quantity
        db.add(user_basket_info)
        db.commit()
    else:
        add_to_basket_model = Basket(
            goods_id = goods_info.id,
            user_id = user.get("id"),
            quantity = request.quantity,
            price_for_the_one = goods_info.price
        )
        db.add(add_to_basket_model)
        db.commit()
        
    

@router.put("/basket-edit",status_code = status.HTTP_200_OK)
async def edit_basket(db: db_dependancy, user: user_dependency, request: EditTheBasketRequest ):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    edit_basket_model = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request.goods_id).first()
    if edit_basket_model is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No goods with such ID in your basket")
    
    model = db.query(Goods).filter(Goods.id == request.goods_id).first()
    if model.quantity < request.new_quantity:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f"We don`t have enought goods. There is only {model.quantity}")

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


@router.post("/order", status_code = status.HTTP_200_OK)
async def create_order(db: db_dependancy, user: user_dependency, order: CreateOrderRequest):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site

    create_order_model = Orders(
        reciever_name = order.reciever_name,
        shipping_adress = order.shipping_adress,
        user_id = user.get("id"),
        total_price = 1
    )
    db.add(create_order_model)
    db.commit()

    total_price = 0

    goods_in_basket = []
    goods_in_basket = db.query(Basket).filter(Basket.user_id == user.get("id")).all()
    for good in goods_in_basket:
        order_item = OrderItem(
            goods_id = good.goods_id,
            quantity = good.quantity,
            order_id = create_order_model.order_number
        )
        total_price += good.quantity * (db.query(Goods).filter(Goods.id == good.goods_id).first()).price
        db.add(order_item)
        db.commit()
        change_goods_quantity_model = db.query(Goods).filter(Goods.id == order_item.goods_id).first()
        change_goods_quantity_model.quantity -= order_item.quantity
        db.add(change_goods_quantity_model)
        db.commit()


    create_order_model.total_price = total_price
    db.add(create_order_model)
    db.commit()
    

    user_info = db.query(Users).filter(Users.id == user.get("id")).first()
    if(user_info.email is not None):
        await send_order_details(user_info.email, create_order_model.order_number, db)
    
    #clear_basket
    for good in goods_in_basket:
        db.query(Basket).filter(Basket.user_id == user.get("id")).filter(good.goods_id == Basket.goods_id).delete()
        db.commit()


@router.put("/cancel-order", status_code = status.HTTP_200_OK)
async def cancel_order(db: db_dependancy, user: user_dependency, order_number: int):
    if user is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site

    order_info = db.query(Orders).filter(Orders.order_number == order_number).filter(Orders.user_id == user.get("id")).first()

    if order_info is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No such order")

    order_items_to_cancel = []
    order_items_to_cancel = db.query(OrderItem).filter(OrderItem.order_id == order_info.order_number).all()
    for item in order_items_to_cancel:
        add_back_to_goods = item.quantity
        good_model = db.query(Goods).filter(Goods.id == item.goods_id).first()
        good_model.quantity += add_back_to_goods
        db.add(good_model)
        db.commit()

        #db.query(OrderItem).filter(OrderItem.goods_id == item.goods_id).filter(OrderItem.order_id == item.order_id).delete()
        #db.commit()

    #db.query(Orders).filter(Orders.order_number == order_info.order_number).delete()
    order_info.status = "canceled"
    db.add(order_info)
    db.commit()
    user_info = db.query(Users).filter(Users.id == user.get("id")).first()
    if(user_info.email is not None):
        await send_cancel_order_notification(user_info.email, order_info.order_number)
    


@router.put("/edit-user-info", status_code = status.HTTP_202_ACCEPTED)
async def edit_user(db: db_dependancy, user: user_dependency, request: EditUserRequest):
    if user is None or user.get("username") is None:
        return {"message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"}
        #here I want to add LocalStorage so user can add goods to the basket without registration 
        #and list of the goods will be stored in the local storage even if user closed the site
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    permission_to_change_email = False
    permission_to_change_number = False

    if request.first_name != "Empty":
        user_model.first_name = request.first_name

    if request.last_name != "Empty":
        user_model.last_name = request.last_name

    if request.email != "Empty":
        if check_if_user_enter_email_or_phone_num(request.email) == "Email":
            is_user_with_such_email_exist = db.query(Users).filter(Users.email == request.email).first()
            if is_user_with_such_email_exist is None:
                permission_to_change_email = True
            else:
                raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "User with such email already exist")
            
    if request.phone_number != "Empty":
        if check_if_user_enter_email_or_phone_num(request.phone_number) == "Phone_number":
            is_user_with_such_number_exist = db.query(Users).filter(Users.phone_number == request.phone_number).first()
            if is_user_with_such_number_exist is None:
                permission_to_change_number = True

            else:
                raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "User with such phone number already exist")

    
    if request.email != "Empty":
        if check_if_user_enter_email_or_phone_num(request.email) == "Something wrong with your email or phone number. Please, check if your information is correct":
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Something wrong with your email. Please, check if your information is correct")
    if request.phone_number != "Empty":
        if check_if_user_enter_email_or_phone_num(request.phone_number) == "Something wrong with your email or phone number. Please, check if your information is correct":
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Something wrong with your phone number. Please, check if your information is correct")
    
    if permission_to_change_number == True:
        user_model.phone_number = request.phone_number
        #need to send verefication SMS

    if permission_to_change_email == True:
        user_model.email = request.email
        user_model.is_active = False
        await send_verification_email(request.email)

    db.add(user_model)
    db.commit()

@router.put("/change-password", status_code = status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependancy, request: RecoverPasswordRequest):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Log in first")
    user_info = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(request.old_password, user_info.hashed_password): 
        raise HTTPException(status_code = status.HTTP_406_NOT_ACCEPTABLE, detail = "Wrong password")
    
    user_info.hashed_password = bcrypt_context.hash(request.new_password)

    db.commit

