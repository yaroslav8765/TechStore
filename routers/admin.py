from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Users, Orders,OrderItem, Smartphones, Goods
from ..routers.auth import get_current_user

router = APIRouter(
    prefix = "/admin-panel",
    tags=["admin-panel"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/show-all-users",status_code= status.HTTP_200_OK )
async def get_all_users(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Users).all()
    return users_to_return

@router.get("/show-all-orders",status_code= status.HTTP_200_OK )
async def get_all_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).all()
    return order_info_to_return

@router.get("/show-new-orders",status_code= status.HTTP_200_OK )
async def show_new_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).filter(Orders.status == "pending").all()
    return order_info_to_return

@router.get("/show-sended-orders",status_code= status.HTTP_200_OK )
async def show_sended_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).filter(Orders.status == "Sended").all()
    return order_info_to_return


@router.get("/show-orders-waites-for-recieving",status_code= status.HTTP_200_OK )
async def show_orders_waites_for_recieving(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).filter(Orders.status == "Waiting for reciever").all()
    return order_info_to_return


@router.get("/show-recieved-orders",status_code= status.HTTP_200_OK )
async def show_recieved_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).filter(Orders.status == "Recieved").all()
    return order_info_to_return

@router.get("/show-users-orders/{user_id}",status_code= status.HTTP_200_OK )
async def show_users_orders(db: db_dependancy, user_id: int, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = []
    order_info_to_return = db.query(Orders).filter(Orders.user_id == user_id).all()
    return order_info_to_return

@router.get("/show-order-info/{order_number}",status_code= status.HTTP_200_OK )
async def show_order_info(db: db_dependancy, order_number: int, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    order_info_to_return = db.query(Orders).filter(Orders.order_number == order_number).first()

    list_of_goods_ids = db.query(OrderItem).filter(OrderItem.order_id == order_info_to_return.order_number).all()
    list_of_goods = []
    for good in list_of_goods_ids:
        list_of_goods.append(db.query(Goods).filter(Goods.id == good.goods_id).first())

    return order_info_to_return, list_of_goods









@router.put("/change-order-status/complecting/", status_code = status.HTTP_202_ACCEPTED)
async def change_order_status_to_complecting(db: db_dependancy, user: user_dependency, order_number: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    oreder_model =  db.query(Orders).filter(Orders.order_number == order_number).first()
    oreder_model.status = "Complecting"
    db.commit()

@router.put("/change-order-status/canecled/", status_code = status.HTTP_202_ACCEPTED)
async def change_order_status_to_canecled(db: db_dependancy, user: user_dependency, order_number: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    oreder_model =  db.query(Orders).filter(Orders.order_number == order_number).first()
    oreder_model.status = "Canceled"
    db.commit()

@router.put("/change-order-status/sended/", status_code = status.HTTP_202_ACCEPTED)
async def change_order_status_to_sended(db: db_dependancy, user: user_dependency, order_number: int):    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    oreder_model =  db.query(Orders).filter(Orders.order_number == order_number).first()
    oreder_model.status = "Sended"
    db.commit()

@router.put("/change-order-status/waiting-for-reciever/", status_code = status.HTTP_202_ACCEPTED)
async def change_order_status_to_waiting_for_reciever(db: db_dependancy, user: user_dependency, order_number: int):    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    oreder_model =  db.query(Orders).filter(Orders.order_number == order_number).first()
    oreder_model.status = "Waiting for reciever"
    db.commit()

@router.put("/change-order-status/recieved/", status_code = status.HTTP_202_ACCEPTED)
async def change_order_status_to_recieved(db: db_dependancy, user: user_dependency, order_number: int):    
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    oreder_model =  db.query(Orders).filter(Orders.order_number == order_number).first()
    oreder_model.status = "Recieved"
    db.commit()