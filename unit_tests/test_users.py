from datetime import datetime
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

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


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
def test_order_and_order_item():
    db = TestingSessionLocal()

    # Убедись, что таблицы существуют
    Base.metadata.create_all(db.bind)

    order = Orders(
        order_number=1,
        user_id = 1,
        reciever_name="Tohru",
        shipping_adress="Miss Kobayashi's Home",
        total_price=4999.45,
        status="pending",
        created_at=datetime.strptime("2025-03-28 13:43:01.143899", "%Y-%m-%d %H:%M:%S.%f"),
        updated_at=datetime.strptime("2025-03-29 17:28:06.922703", "%Y-%m-%d %H:%M:%S.%f"),
    )
    order_item = OrderItem(
        id=1,
        order_id=1,
        goods_id=2,
        quantity=5
    )
    db.add(order)
    db.add(order_item)
    db.commit()

    try:
        yield order, order_item
    finally:
        db.query(OrderItem).delete()
        db.query(Orders).delete()
        db.commit()



@pytest.fixture
def test_user():
    user = Users(
        id = 1,
        email = "pechorkin2014@gmail.com",
        first_name = "Yaroslav",
        last_name = "Pechorkin",
        phone_number = "+380637014924",
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

@pytest.fixture
def test_unauthorized_user():
    user = Users(
        id = 1,
        email = "pechorkin2014@gmail.com",
        first_name = "Yaroslav",
        last_name = "Pechorkin",
        hashed_password = "35bu35jv5v7jv567jv6347j44j",
        is_active = True,
        role = "unknown",

    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()        

@pytest.fixture
def test_admin_user():
    user = Users(
        id = 1,
        email = "pechorkin2014@gmail.com",
        first_name = "Yaroslav",
        last_name = "Pechorkin",
        hashed_password = "35bu35jv5v7jv567jv6347j44j",
        is_active = True,
        role = "admin",

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
    try:
        response = client.post("/user/add-to-basket", json = request_data)
        assert response.status_code == status.HTTP_201_CREATED

        user = {"username": "pechorkin2014@gmail.com", "id": 1, "role": "user"}
        db = TestingSessionLocal()
        model = db.query(Basket).filter(Basket.user_id == user.get("id")).filter(Basket.goods_id == request_data.get("goods_id")).first()
        assert model.user_id == user.get("id")
        assert model.quantity == request_data.get("quantity") + (test_basket.quantity - request_data.get("quantity"))
        assert model.goods_id == request_data.get("goods_id")
        assert model.price_for_the_one == test_good.price
    finally:
        db = TestingSessionLocal()
        db.query(Basket).delete()
        db.commit()
        db.close()

def test_add_to_the_basket_unexisting_item(test_good):
    request_data = {
        "goods_id": 999,
        "quantity": 5,
        }
    try:
        response = client.post("/user/add-to-basket", json = request_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "No goods with such ID"}
    finally:
        db = TestingSessionLocal()
        db.query(Basket).delete()
        db.commit()
        db.close()


def test_add_to_the_basket_more_than_exist(test_good):
    request_data = {
        "goods_id": 2,
        "quantity": 500,
        }
    try:
        response = client.post("/user/add-to-basket", json = request_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "We don`t have enought goods. There is only 23"}
    finally:
        db = TestingSessionLocal()
        db.query(Basket).delete()
        db.commit()
        db.close()

def test_add_to_the_basket_user_is_none(test_good):
    request_data = {
        "goods_id": 2,
        "quantity": 5,
    }

    app.dependency_overrides[get_current_user] = lambda: None

    try:
        response = client.post("/user/add-to-basket", json=request_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"
        }
    finally:
        db = TestingSessionLocal()
        db.query(Basket).delete()
        db.commit()
        db.close()
        app.dependency_overrides[get_current_user] = override_get_current_user



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

def test_create_order(test_basket, test_good, test_user):
    request_data = {
        "reciever_name": "Tohru",
        "shipping_adress": "Miss Kobayashi's Home"
    }
    try:
        db = TestingSessionLocal()
        goods_in_basket = db.query(Basket).filter(Basket.user_id == test_user.id).count()

        response = client.post("/user/order", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        
        created_order = db.query(Orders).filter(Orders.user_id == test_user.id).first()
        assert created_order is not None
        assert created_order.reciever_name == request_data["reciever_name"]
        assert created_order.shipping_adress == request_data["shipping_adress"]
        assert created_order.total_price > 0

        order_items = db.query(OrderItem).filter(OrderItem.order_id == created_order.order_number).all()
        assert len(order_items) == goods_in_basket
        
        basket_empty = db.query(Basket).filter(Basket.user_id == test_user.id).count() == 0
        assert basket_empty
    finally:
        db = TestingSessionLocal()
        db.query(OrderItem).delete()
        db.query(Orders).delete()
        db.commit()
        db.close()


def test_create_order_no_user():
    request_data = {
        "reciever_name": "Tohru",
        "shipping_adress": "Miss Kobayashi's Home"
    }
    try:
        app.dependency_overrides[get_current_user] = lambda: None

        response = client.post("/user/order", json=request_data)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "message": "Sorry, but at this moment if you want to add good to the basket you need to create accout first"
        }

        app.dependency_overrides[get_current_user] = override_get_current_user
    finally:
        db = TestingSessionLocal()
        db.query(OrderItem).delete()
        db.query(Orders).delete()
        db.commit()
        db.close()

#############################################################################
#                                                                           #
#                               Cancel order                                #
#                                                                           #
#############################################################################

def test_cancel_order(test_good, test_order_and_order_item, test_user):
    response = client.put("/user/cancel-order", params={"order_number": 1})

    assert response.status_code == 200

#############################################################################
#                                                                           #
#                             Edit users info                               #
#                                                                           #
#############################################################################

def test_edit_users_info(test_user):
    request_data = {
        "First_name": "NewFirstName",
        "Last_name": "NewLastName",
        "email": "golovachlena1892@gmail.com",
        "phone_number": "+380937085111",
    }

    response = client.put("/user/edit-user-info", json=request_data)
    db = TestingSessionLocal()
    assert response.status_code == status.HTTP_202_ACCEPTED
    updated_user = db.query(Users).filter(Users.id == test_user.id).first()
    assert updated_user.first_name == "NewFirstName"
    assert updated_user.last_name == "NewLastName"
    assert updated_user.email == "golovachlena1892@gmail.com"
    assert updated_user.phone_number == "+380937085111"

def test_edit_users_info_email_exist(test_user):
    request_data = {
        "First_name": "NewFirstName",
        "Last_name": "NewLastName",
        "email": "pechorkin2014@gmail.com",
        "phone_number": "+380937085111",
    }
    
    response = client.put("/user/edit-user-info", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "User with such email already exist"}

def test_edit_users_info_phone_num_exist(test_user):
    request_data = {
        "First_name": "NewFirstName",
        "Last_name": "NewLastName",
        "email": "golovachlena1892@gmail.com",
        "phone_number": "+380637014924",
    }
    
    response = client.put("/user/edit-user-info", json=request_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {"detail": "User with such phone number already exist"}

def test_edit_users_info_invalid_email(test_user):
    request_data = {
        "First_name": "NewFirstName",
        "Last_name": "NewLastName",
        "email": "vasya@chernv.com",
        "phone_number": "+380937085111",
    }
    
    response = client.put("/user/edit-user-info", json=request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Something wrong with your email. Please, check if your information is correct"}

def test_edit_users_info_invalid_phone_num(test_user):
    request_data = {
        "First_name": "NewFirstName",
        "Last_name": "NewLastName",
        "email": "golovachlena1892@gmail.com",
        "phone_number": "52672547245",
    }
    
    response = client.put("/user/edit-user-info", json=request_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Something wrong with your phone number. Please, check if your information is correct"}