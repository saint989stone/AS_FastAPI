from src.repositories.base import BaseRepo
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room

class RoomsRepo(BaseRepo):
    model = RoomsORM
    schema = Room