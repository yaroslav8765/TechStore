from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ...models import Users, OrderItem, Orders, Goods
from ...config import settings
from starlette import status


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy = Annotated[Session, Depends(get_db)]

class OrderItemToReturn: 
    Name: str
    Price_for_one: float
    Quantity: int
    Total_price: int

    def __init__ (self, Name, Price_for_one, Quantity, Total_price):
        self.Name = Name
        self.Price_for_one = Price_for_one
        self.Quantity = Quantity
        self.Total_price = Total_price

conf = ConnectionConfig(
    MAIL_USERNAME="pechorkin2014@gmail.com",
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="pechorkin2014@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False  
)


async def send_order_details(email: str, order_id: int, db: db_dependancy):
    list_of_orders = []
    list_of_goods = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    order_info = db.query(Orders).filter(Orders.order_number == order_id).first()
    total_for_order = 0
    for good in list_of_goods:
        goods_info = db.query(Goods).filter(Goods.id == good.goods_id).first()
        list_of_orders.append(OrderItemToReturn(
            Name = goods_info.name,
            Price_for_one = goods_info.price,
            Quantity = good.quantity,
            Total_price = goods_info.price * good.quantity
        ))
        total_for_order += (goods_info.price * good.quantity)


    orders_text = "    ".join(
        [f"{item.Name} - {item.Quantity} pieces x {item.Price_for_one} = {item.Total_price} \n" for item in list_of_orders]
    )


    message_body = f"""
    Your order details:
    
    {orders_text}
    
    Total price: {total_for_order}
    Receiver name: {order_info.reciever_name}
    Shipping address: {order_info.shipping_adress}
    """


    message = MessageSchema(
        subject=f"TechStore. Order №{order_id} info",
        recipients=[email],
        body=message_body,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_cancel_order_notification(email: str, order_id: int):

    message = MessageSchema(
        subject="TechStore. Order cancelation notification",
        recipients=[email],
        body=f"You just cancen order {order_id}. Hope to have new orders from you :) ",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)