"""
Базовый класс репозиториев
"""
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from src.database import engine


class BaseRepo:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        print(engine, query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(engine, stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def delete(self, **filter_by) -> None:
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        print(engine, stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool=False, **filter_by) -> None:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))         #exclude_unset позволяет не передавать данные которые не переданы пользователем используется при частичном обновлении в базе данных
        )
        print(engine, stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)