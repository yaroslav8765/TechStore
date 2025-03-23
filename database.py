from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
#create_engine — создаёт подключение к базе данных.
#sessionmaker — создаёт фабрику сессий для работы с БД.
#declarative_base — базовый класс для создания моделей SQLAlchemy.

SQLALCHEMY_DATABASE_URL = "postgresql://neondb_owner:npg_17yhrwEjFAcf@ep-white-wave-a2bks9f9-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require" 
#строка подключения к PostgreSQL

engine = create_engine(SQLALCHEMY_DATABASE_URL) #создать движок для взаимодействия с базой данных

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine) # cоздание сессии
#autocommit=False — изменения в базе фиксируются вручную (session.commit()).
#autoflush=False — не отправлять изменения в БД автоматически перед запросами.
#bind=engine — привязывает сессию к engine.

Base = declarative_base() #базовый класс, от которого наследуются все модели

