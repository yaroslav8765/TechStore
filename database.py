from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings
#create_engine — создаёт подключение к базе данных.
#sessionmaker — создаёт фабрику сессий для работы с БД.
#declarative_base — базовый класс для создания моделей SQLAlchemy.

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL) #создать движок для взаимодействия с базой данных

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) # cоздание сессии
#autocommit=False — изменения в базе фиксируются вручную (session.commit()).
#autoflush=False — не отправлять изменения в БД автоматически перед запросами.
#bind=engine — привязывает сессию к engine.

Base = declarative_base() #базовый класс, от которого наследуются все модели

