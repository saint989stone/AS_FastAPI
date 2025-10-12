from celery.bin.result import result
from fastapi import APIRouter, Body
from passlib.context import CryptContext
from src.database import async_session_maker
from src.repositories.users import UsersRepo
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def create_user(data: UserRequestAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Bob",
            "value": {
                "email": "bob@mail.ru",
                "password": "1qaz@WSX",
            },
        },
        "2": {
            "summary": "Cat",
            "value": {
                "email": "cat@mail.ru",
                "password": "1qaz@WSX",
            },
        },
    })
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        res = await UsersRepo(session).add(new_user_data)
        await session.commit()
        if res:
            return {"status": "OK"}
        else:
            return {"status": "ERROR"}