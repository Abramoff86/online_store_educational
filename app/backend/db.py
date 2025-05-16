from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase



DB_HOST = 'localhost'
DB_PORT = '5433'
DB_NAME = 'ecommerce'
DB_USER = 'ecommerce'
DB_PASSWORD = 'xxxxx' #указать свое и спрятать, тут просто для примера

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass