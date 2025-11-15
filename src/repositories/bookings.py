from datetime import date

from celery.bin.result import result

from src.repositories.base import BaseRepo
from src.models.bookings import BookingsORM
from sqlalchemy import select

from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepo(BaseRepo):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_today_checkin(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        result = self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]