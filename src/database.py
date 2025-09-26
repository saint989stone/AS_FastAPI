import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

class Base(DeclarativeBase):
    pass

async def get_version():
    async with engine.begin() as connection:
        result = await connection.execute(text("SELECT version()"))
        print(result.fetchone())

asyncio.run(get_version())