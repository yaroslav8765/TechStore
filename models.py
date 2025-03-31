from .database import Base
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from datetime import datetime, timezone, timedelta

utc_plus_2 = timezone(timedelta(hours=2))

class Users(Base):
    __tablename__ = 'users'

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True)
    phone_number    = Column(String, unique=True)
    first_name      = Column(String)
    last_name       = Column(String)
    hashed_password = Column(String)
    is_active       = Column(Boolean, default=True)
    role            = Column(String)

class Goods(Base):
    __tablename__ = 'goods'

    id                      = Column(Integer, primary_key=True, index=True)
    name                    = Column(String)
    price                   = Column(Float)
    description             = Column(String)
    category                = Column(String)
    quantity                = Column(Integer, default=0)
    image_url               = Column(String)
    characteristics_table   = Column(String)

    
class Smartphones(Base):
    __tablename__ = "smartphones"

    id                      = Column(Integer, primary_key=True, index=True)
    goods_id                = Column(Integer, ForeignKey("goods.id"))
    Display_diagonal        = Column(Float)
    Screen_resolution       = Column(String)
    Screen_type             = Column(String, default=None)
    Screen_refresh_rate     = Column(String, default=None)
    Communication_standards = Column(String)
    Number_of_SIM_cards     = Column(Integer)
    SIM_card_size           = Column(String)
    e_SIM_support           = Column(Boolean)
    Processor_Model         = Column(String, default=None)
    Number_of_Cores         = Column(Integer, default=None)
    RAM                     = Column(String, default=None)
    Built_in_Memory         = Column(String)
    Expandable_Memory       = Column(String, default=None)
    Main_camera             = Column(String, default=None)
    Front_camera            = Column(String, default=None)
    Maximum_video_resolution= Column(String, default=None)
    Stabilization           = Column(String, default=None)
    Wi_Fi_Standards         = Column(String, default=None)
    Bluetooth               = Column(String, default=None)
    Navigation_System       = Column(String, default=None)
    NFC                     = Column(Boolean, default=None)
    USB_Interface           = Column(String, default=None)
    Battery_capacity        = Column(String, default=None)
    Height                  = Column(Integer)
    Width                   = Column(Integer)
    Depth                   = Column(Integer)
    Weight                  = Column(Integer)
    Manufacturer_color      = Column(String)
    Warranty_period         = Column(String) 
    Country_of_manufacture  = Column(String)
    Brand = Column(String)

class Laptops(Base):
    __tablename__ = "laptops"

    id                      = Column(Integer, primary_key=True, index=True)
    goods_id                = Column(Integer, ForeignKey("goods.id"))
    Display_diagonal        = Column(Float)
    Screen_resolution       = Column(String)
    Screen_type             = Column(String, default=None)
    Screen_refresh_rate     = Column(String, default=None)
    Processor_Model         = Column(String)
    Number_of_Cores         = Column(Integer)
    RAM                     = Column(String)
    Built_in_Memory         = Column(String)
    Expandable_Memory       = Column(String, default=None)
    GPU_Model               = Column(String, default=None)
    VRAM                    = Column(String, default=None)
    Main_camera             = Column(String, default=None)
    Front_camera            = Column(String, default=None)
    Maximum_video_resolution= Column(String, default=None)
    Wi_Fi_Standards         = Column(String, default=None)
    Bluetooth               = Column(String, default=None)
    USB_Ports               = Column(String, default=None)
    HDMI_Port               = Column(Boolean, default=None)
    Thunderbolt_Support     = Column(Boolean, default=None)
    Battery_capacity        = Column(String, default=None)
    Battery_life            = Column(String, default=None)
    Height                  = Column(Integer)
    Width                   = Column(Integer)
    Depth                   = Column(Integer)
    Weight                  = Column(Integer)
    Manufacturer_color      = Column(String)
    Warranty_period         = Column(String) 
    Country_of_manufacture  = Column(String)
    Brand                   = Column(String)

class Basket(Base):
    __tablename__ = "basket"
    id                      = Column(Integer, primary_key=True, index=True)  
    goods_id                = Column(Integer, ForeignKey("goods.id"))
    user_id                 = Column(Integer, ForeignKey("users.id"))
    quantity                = Column(Integer)
    price_for_the_one       = Column(Float)

class Orders(Base):
    __tablename__ = "orders"

    order_number    = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, ForeignKey("users.id"))
    reciever_name   = Column(String)
    shipping_adress = Column(String)
    total_price     = Column(Float, nullable=False)
    status          = Column(String, default="pending")
    created_at      = Column(DateTime, default=datetime.now(utc_plus_2))
    updated_at      = Column(DateTime, default=datetime.now(utc_plus_2), onupdate=datetime.now(utc_plus_2))

class OrderItem(Base):
    __tablename__ = "order_item"

    id              = Column(Integer, primary_key=True, index=True)  
    order_id        = Column(Integer, ForeignKey("orders.order_number"))
    goods_id        = Column(Integer, ForeignKey("goods.id"))
    quantity        = Column(Integer)