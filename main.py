from fastapi import FastAPI
from database import engine
from models import Base
from routers import auth, email_verification, admin
app = FastAPI()

Base.metadata.create_all(bind = engine) #создать таблицы в БД, если их ещё нема

try:
    engine.connect()
    print("✅ Подключение успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")

@app.get("/")
async def test():
    return{"message": "Hello World"}

app.include_router(auth.router)
app.include_router(email_verification.router)
app.include_router(admin.router)