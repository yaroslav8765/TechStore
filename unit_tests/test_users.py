import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.users import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from ..models import Smartphones, Laptops, Orders, OrderItem, Basket, Goods, Users

SQLALCHEMY_DATABESE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABESE_URL, 
    connect_args = {"check_same_thread":False},
    poolclass = StaticPool,

)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally: 
        db.close()

def override_get_current_user():
    return {"username": "pechorkin2014@gmail.com", "id": 1, "role": "user"}

    
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_basket():
    basket = Basket(
        id = 1,
        goods_id = 2,
        user_id = 1,
        quantity = 3,
        price_for_the_one = 999.89
    )

    db = TestingSessionLocal()
    db.add(basket)
    db.commit()
    yield basket
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM basket;"))
        connection.commit()

@pytest.fixture
def test_good():
    good = Goods(
        id = 2,
        name = "Xiaomi 14 Ultra",
        price = 999.89,
        description = "Ultra-premium smartphone with a focus on photography and performance.",
        category = "Smartphones",
        quantity = "23",
        image_url = "https://example.com/images/xiaomi_14_ultra.jpg",
        characteristics_table = "smartphones",
    )

    db = TestingSessionLocal()
    db.add(good)
    db.commit()
    yield good
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM goods;"))
        connection.commit()       

@pytest.fixture
def test_user():
    user = Users(
        id = 1,
        email = "pechorkin2014@gmail.com",
        first_name = "Yaroslav",
        last_name = "Pechorkin",
        hashed_password = "35bu35jv5v7jv567jv6347j44j",
        is_active = True,
        role = "user",

    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()             


#############################################################################
#                                                                           #
#                           Show users basket                               #
#                                                                           #
#############################################################################

def test_show_users_basket(test_basket):
    response = client.get("/user/show-basket")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "goods_id": 2,"user_id": 1,"quantity": 3, "price_for_the_one": 999.89 }]


#############################################################################
#                                                                           #
#                           Add to the basket                               #
#                                                                           #
#############################################################################

def test_add_to_the_basket(test_basket, test_good):
    request_data = {
        "goods_id": 2,
        "quantity": 5,
        }
    response = client.post("/user/add-to-basket", json = request_data)
    assert response.status_code == status.HTTP_201_CREATED

    user = {"username": "pechorkin2014@gmail.com", "id": 1, "role": "user"}
    db = TestingSessionLocal()
    model = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request_data.get("goods_id")).first()
    assert model.user_id == user.get("id")
    assert model.quantity == request_data.get("quantity") + (test_basket.quantity - request_data.get("quantity"))
    assert model.goods_id == request_data.get("goods_id")
    assert model.price_for_the_one == test_good.price

def test_add_to_the_basket_unexisting_item(test_good):
    request_data = {
        "goods_id": 999,
        "quantity": 5,
        }
    response = client.post("/user/add-to-basket", json = request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_add_to_the_basket_more_than_exist(test_good):
    request_data = {
        "goods_id": 2,
        "quantity": 500,
        }
    response = client.post("/user/add-to-basket", json = request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


#############################################################################
#                                                                           #
#                           Edit users basket                               #
#                                                                           #
#############################################################################

def test_edit_basket(test_basket, test_good):
    request_data = {
        "goods_id": 2,
        "new_quantity": 10,
        }
    response = client.put("/user/basket-edit", json = request_data)
    assert response.status_code == status.HTTP_200_OK

    user = {"username": "pechorkin2014@gmail.com", "id": 1, "role": "user"}
    db = TestingSessionLocal()
    model = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request_data.get("goods_id")).first()
    assert model.user_id == user.get("id")
    assert model.quantity == request_data.get("new_quantity")
    assert model.goods_id == request_data.get("goods_id")
    assert model.price_for_the_one == test_basket.price_for_the_one

def test_edit_basket_invalid_id(test_basket, test_good):
    request_data = {
        "goods_id": 999,
        "new_quantity": 10,
        }
    response = client.put("/user/basket-edit", json = request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_edit_basket_invalid_quantity(test_basket, test_good):
    request_data = {
        "goods_id": 2,
        "new_quantity": 999,
        }
    response = client.put("/user/basket-edit", json = request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


#############################################################################
#                                                                           #
#                           Delete from the basket                          #
#                                                                           #
#############################################################################

def test_delete_goods_from_basket(test_basket, test_good):

    response = client.delete("/user/basket-delete-good?goods_id=2")
    assert response.status_code == status.HTTP_202_ACCEPTED
    db = TestingSessionLocal()
    info = db.query(Basket).filter(Basket.user_id == 1).all()
    assert info == []

#############################################################################
#                                                                           #
#                               Create order                                #
#                                                                           #
#############################################################################

def test_create_order(test_basket, test_good,test_user):
    request_data = {
        "reciever_name": "Tohru",
        "shipping_adress": "Miss Kobayashi's Home"
    }
    response = client.post("/user/order", json = request_data)
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Orders).filter(Orders.order_number == test_user.id).all()
    assert model == [{"....."}]