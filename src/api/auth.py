from fastapi import APIRouter, Body, HTTPException, Response
from src.database import async_session_maker
from src.repositories.users import UsersRepo
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/login")
async def login(response: Response,
                data: UserRequestAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Bob",
            "value": {
                "email": "bob@mail.ru",
                "password": "1qaz@WSX",
            },
        }
    })
):
    async with async_session_maker() as session:
        user = await UsersRepo(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегестрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}


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
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepo(session).add(new_user_data)
        await session.commit()

@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepo(session).get_one_or_none(id=user_id)
        return user