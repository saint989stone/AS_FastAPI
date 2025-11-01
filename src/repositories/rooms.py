from datetime import date

from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepo
from src.models.rooms import RoomsORM
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room

class RoomsRepo(BaseRepo):
    model = RoomsORM
    schema = Room

    async def get_filtred_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        #print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return await self.get_filtred(RoomsORM.id.in_(rooms_ids_to_get))