from src.repositories.base import BaseRepo
from src.models.rooms import RoomsORM

class RoomsRepo(BaseRepo):
    model = RoomsORM