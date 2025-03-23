from fastapi import FastAPI
from database import engine
from models import Base
from routers import admin
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

