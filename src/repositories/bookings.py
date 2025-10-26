from src.repositories.base import BaseRepo
from src.models.bookings import BookingsORM
from sqlalchemy import select
from src.schemas.bookings import Booking


class BookingsRepo(BaseRepo):
    model = BookingsORM
    schema = Booking