from src.repositories.base import BaseRepo
from src.models.bookings import BookingsORM
from sqlalchemy import select

from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepo(BaseRepo):
    model = BookingsORM
    mapper = BookingDataMapper