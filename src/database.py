import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

engine = create_async_engine(settings.DB_URL, echo=False)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

class Base(DeclarativeBase):
    pass