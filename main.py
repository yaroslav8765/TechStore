from fastapi import FastAPI
from database import engine
from models import Base
from routers import auth, admin, users
from routers.goods_actions import goods_actions_user, goods_actions_admin
from routers.email_actions import email_verification
app = FastAPI()

Base.metadata.create_all(bind = engine) #создать таблицы в БД, если их ещё нема

try:
    engine.connect()
    print("✅ Подключение успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")



from routers.auth import check_if_user_enter_email_or_phone_num
@app.get("/{test_login}")
async def test(test_login:str):
    return check_if_user_enter_email_or_phone_num(test_login)
    return{"message": "Hello World"}

app.include_router(auth.router)
app.include_router(email_verification.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(goods_actions_admin.router)