from src.repositories.base import BaseRepo
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facility, RoomFacility

class FacilitiesRepo(BaseRepo):
    model = FacilitiesORM
    schema = Facility

class RoomsFacilitiesRepo(BaseRepo):
    model = RoomsFacilitiesORM
    schema = RoomFacility