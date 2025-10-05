from src.repositories.base import BaseRepo
from src.models.hotels import HotelsORM
from sqlalchemy import select


class HotelsRepo(BaseRepo):
    model = HotelsORM

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ):
        query = select(self.model)
        if title:
            query = query.filter(HotelsORM.title.ilike('%' + title + '%'))          #против SQL иньекции можно использовать метод contains
        if location:
            query = query.filter(HotelsORM.location.ilike('%' + location + '%'))
        query = (
            query
            .limit(limit)         #количество записей на одной страницы
            .offset(offset)         #сдвиг записей на странице, то есть скакой записи начинается страница
        )
        result = await self.session.execute(query)
        return result.scalars().all()