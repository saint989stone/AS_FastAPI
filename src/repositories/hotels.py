from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepo
from src.models.hotels import HotelsORM
from sqlalchemy import select
from datetime import date
from src.repositories.utils import rooms_ids_for_booking
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

    async def get_filtred_by_time(
            self,
            date_from: date,
            date_to: date,
            title,
            location,
            limit,
            offset,
    )-> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        query = select(self.model).filter(HotelsORM.id.in_(hotels_ids_to_get))
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



        #print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtred(HotelsORM.id.in_(hotels_ids_to_get))