from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ...models import Users, Orders, Smartphones, Laptops, Goods 
from ...routers.auth import get_current_user
from ...routers.goods_actions.request_models.smartphone import AddEditSmartphoneRequest, add_smartphones_model, edit_smartphone_model
from ...routers.goods_actions.request_models.laptop import AddEditLaptopRequest, add_laptop_model, edit_laptop_model

router = APIRouter(
    prefix = "/admin-panel",
    tags=["good_actions_admin"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class AddEditGoodsRequest(BaseModel):
    name: str
    price: float
    description: str
    category: str
    quantity: int = 0
    image_url: str
    characteristics_table: str

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "name" : "Empty", 
                "price" : -1,
                "description" : "Empty",
                "category" : "Empty", 
                "quantity" : -1,
                "image_url" : "Empty",
                "characteristics_table" : "Empty"
            }
        }
    }

def add_goods_model(goods_request: AddEditGoodsRequest):
    add_goods_model = Goods(
        name=goods_request.name,
        price=goods_request.price,
        description=goods_request.description,
        category=goods_request.category,
        quantity=goods_request.quantity,
        image_url=goods_request.image_url,
        characteristics_table = goods_request.characteristics_table
    )
    return add_goods_model

def edit_goods_model(goods_request: AddEditGoodsRequest, old_good: Goods):
    update_fields = {
        "name": "Empty",
        "price": -1,
        "description": "Empty",
        "category": "Empty",
        "quantity": -1,
        "image_url": "Empty",
        "characteristics_table": "Empty",
    }

    for field, empty_value in update_fields.items():
        new_value = getattr(goods_request, field, empty_value)
        if new_value != empty_value:
            setattr(old_good, field, new_value)

    return old_good






##################################################################
#                                                                # 
#                          ADD & EDIT                            # 
#                           DIFFERETN                            # 
#                             GOODS                              # 
#                            SECTION                             # 
#                                                                # 
##################################################################



#############################################################################################################
#                                                                                                           #
#                                                Smartphones                                                #
#                                                                                                           #
#############################################################################################################
@router.post("/add-goods/smartphone", status_code = status.HTTP_201_CREATED)
async def add_smartphone_to_the_db(db: db_dependancy, user: user_dependency, characteristics_request: AddEditSmartphoneRequest, goods_request: AddEditGoodsRequest):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    add_goods = add_goods_model(goods_request)
    db.add(add_goods)
    db.commit()

    new_goods_id = db.query(Goods).filter(Goods.name == goods_request.name, 
                                          Goods.price == goods_request.price, 
                                          Goods.description == goods_request.description).first()
    
    add_smartphone_model = add_smartphones_model(characteristics_request, new_goods_id.id)
    db.add(add_smartphone_model)
    db.commit()


@router.put("/edit-goods/smartphone", status_code = status.HTTP_200_OK)
async def edit_smartphone_in_db(db: db_dependancy, user: user_dependency, characteristics_request: AddEditSmartphoneRequest, goods_request: AddEditGoodsRequest, goods_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    old_good = db.query(Goods).filter(Goods.id == goods_id).first()
    if old_good is None:
        raise HTTPException(status_code=404, detail='Good not found')
    edit_goods_model(goods_request, old_good)
    db.commit()

    old_smartphone = db.query(Smartphones).filter(Smartphones.goods_id == old_good.id).first()
    if old_smartphone is None:
        raise HTTPException(status_code=404, detail='Good not found')
    edit_smartphone_model(characteristics_request, old_smartphone)
    db.commit()


#############################################################################################################
#                                                                                                           #
#                                                Laptops                                                    #
#                                                                                                           #
#############################################################################################################
@router.post("/add-goods/laptop", status_code = status.HTTP_201_CREATED)#                              Laptop                                   
async def add_laptop_to_the_db(db: db_dependancy, user: user_dependency, characteristics_request: AddEditLaptopRequest, goods_request: AddEditGoodsRequest):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    add_goods = add_goods_model(goods_request)
    db.add(add_goods)
    db.commit()

    new_goods_id = db.query(Goods).filter(Goods.name == goods_request.name, 
                                          Goods.price == goods_request.price, 
                                          Goods.description == goods_request.description).first()
    
    add_smartphone_model = add_laptop_model(characteristics_request, new_goods_id.id)
    db.add(add_smartphone_model)
    db.commit()


@router.put("/edit-goods/laptop", status_code = status.HTTP_200_OK)#                                    Laptop         
async def edit_laptop_in_db(db: db_dependancy, user: user_dependency, characteristics_request: AddEditLaptopRequest, goods_request: AddEditGoodsRequest, goods_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    old_good = db.query(Goods).filter(Goods.id == goods_id).first()
    if old_good is None:
        raise HTTPException(status_code=404, detail='Good not found')
    edit_goods_model(goods_request, old_good)
    db.commit()

    old_smartphone = db.query(Laptops).filter(Laptops.goods_id == old_good.id).first()
    if old_smartphone is None:
        raise HTTPException(status_code=404, detail='Good not found')
    edit_laptop_model(characteristics_request, old_smartphone)
    db.commit()