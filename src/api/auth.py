from debugpy.adapter import access_token
from fastapi import APIRouter, Body, HTTPException, Response, Request
from src.database import async_session_maker
from src.repositories.users import UsersRepo
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/login")
async def login(
        data: UserRequestAdd,
        response: Response
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

@router.get("/only_auth")
async def only_auth(
        request: Request,
):
    cookies = request.cookies
    if cookies:
        access_token = cookies["access_token"]
    else:
        access_token = None
    print(access_token)