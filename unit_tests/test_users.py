import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.users import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status

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



class User:
    def __init__(self, id: int, email: str, phone_number: str, first_name: str, last_name: str, hashed_password: str, is_active: bool, role: str):
        self.id = id
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.hashed_password = hashed_password
        self.last_name = last_name
        self.is_active = is_active
        self.role = role

@pytest.fixture
def admin_user():
    return User(1,"pechorkin2014@gmail.com","+380637014924","Yaroslav","Pechorkin","$2b$12$UDEacrZCnoAygNiJcunqm.NLfmWLtFBT/4yCHapOKWToY8sZmhpXm", True, "admin")



def test_user_initialization(admin_user):
    assert admin_user.first_name == "Yaroslav"


def test_show_users_basket():
    response = client.get("/user/show-basket")
    print(response.json()) 
    assert response.status_code == status.HTTP_200_OK