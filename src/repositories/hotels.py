from src.repositories.base import BaseRepo
from src.models.hotels import HotelsORM
from sqlalchemy import select
from src.schemas.hotels import Hotel


class HotelsRepo(BaseRepo):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset,
    ) -> list[Hotel]:
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
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]