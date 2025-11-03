from src.repositories.base import BaseRepo
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import Facilities

class FacilitiesRepo(BaseRepo):
    model = FacilitiesORM
    schema = Facilities