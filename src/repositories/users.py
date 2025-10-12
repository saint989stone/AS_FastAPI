from src.repositories.base import BaseRepo
from src.models.users import UsersORM
from src.schemas.users import User


class UsersRepo(BaseRepo):
    model = UsersORM
    schema = User