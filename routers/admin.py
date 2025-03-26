from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users, Orders, Smartphones
from routers.auth import get_current_user
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

class AddSmartphoneRequest(BaseModel):
    name: str
    price: float
    description: str
    category: str
    quantity: int = 0
    image_url: str

    Display_diagonal: float
    Screen_resolution: str
    Screen_type: Optional[str] = None
    Screen_refresh_rate: Optional[str] = None
    Communication_standards: str
    Number_of_SIM_cards: int
    SIM_card_size: str
    e_SIM_support: bool
    Processor_Model: Optional[str] = None
    Number_of_Cores: Optional[int] = None
    RAM: Optional[str] = None
    Built_in_Memory: str
    Expandable_Memory: Optional[str] = None
    Main_camera: Optional[str] = None
    Front_camera: Optional[str] = None
    Maximum_video_resolution: Optional[str] = None
    Stabilization: Optional[str] = None
    Wi_Fi_Standards: Optional[str] = None
    Bluetooth: Optional[str] = None
    Navigation_System: Optional[str] = None
    NFC: Optional[bool] = None
    USB_Interface: Optional[str] = None
    Battery_capacity: Optional[str] = None
    Height: int
    Width: int
    Depth: int
    Weight: int
    Manufacturer_color: str
    Warranty_period: str
    Country_of_manufacture: str
    Brand: str




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
    users_to_return = []
    users_to_return = db.query(Orders).all()
    return users_to_return

@router.get("/show-new-orders",status_code= status.HTTP_200_OK )
async def show_new_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Orders).filter(Orders.status == "pending").all()
    return users_to_return

@router.get("/show-sended-orders",status_code= status.HTTP_200_OK )
async def show_sended_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Orders).filter(Orders.status == "sended").all()
    return users_to_return

@router.get("/show-recieved_orders",status_code= status.HTTP_200_OK )
async def show_recieved_orders(db: db_dependancy, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Orders).filter(Orders.status == "recieved").all()
    return users_to_return

@router.get("/show-users-order/{user_id}",status_code= status.HTTP_200_OK )
async def show_users_orders(db: db_dependancy, user_id: int, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Orders).filter(Orders.user_id == user_id).all()
    return users_to_return

@router.get("/show-order-info/{order_number}",status_code= status.HTTP_200_OK )
async def show_order_info(db: db_dependancy, order_number: int, user: user_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    users_to_return = []
    users_to_return = db.query(Orders).filter(Orders.order_number == order_number).all()
    return users_to_return

@router.post("/add-goods/smartphone", status_code = status.HTTP_201_CREATED)
async def add_goods_to_the_database(db: db_dependancy, user: user_dependency, request: AddSmartphoneRequest):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    add_smartphone_model = Smartphones(
        name=request.name,
        price=request.price,
        description=request.description,
        category=request.category,
        quantity=request.quantity,
        image_url=request.image_url,
        Display_diagonal=request.Display_diagonal,
        Screen_resolution=request.Screen_resolution,
        Screen_type=request.Screen_type,
        Screen_refresh_rate=request.Screen_refresh_rate,
        Communication_standards=request.Communication_standards,
        Number_of_SIM_cards=request.Number_of_SIM_cards,
        SIM_card_size=request.SIM_card_size,
        e_SIM_support=request.e_SIM_support,
        Processor_Model=request.Processor_Model,
        Number_of_Cores=request.Number_of_Cores,
        RAM=request.RAM,
        Built_in_Memory=request.Built_in_Memory,
        Expandable_Memory=request.Expandable_Memory,
        Main_camera=request.Main_camera,
        Front_camera=request.Front_camera,
        Maximum_video_resolution=request.Maximum_video_resolution,
        Stabilization=request.Stabilization,
        Wi_Fi_Standards=request.Wi_Fi_Standards,
        Bluetooth=request.Bluetooth,
        Navigation_System=request.Navigation_System,
        NFC=request.NFC,
        USB_Interface=request.USB_Interface,
        Battery_capacity=request.Battery_capacity,
        Height=request.Height,
        Width=request.Width,
        Depth=request.Depth,
        Weight=request.Weight,
        Manufacturer_color=request.Manufacturer_color,
        Warranty_period=request.Warranty_period,
        Country_of_manufacture=request.Country_of_manufacture,
        Brand=request.Brand,
    )

    db.add(add_smartphone_model)
    db.commit()