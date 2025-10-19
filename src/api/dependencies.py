from typing import Annotated
from fastapi import Depends, Query, HTTPException, Request
from pydantic import BaseModel
from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(default=5, description="Количество элементов на странице", ge=1, le=30)]
PaginationDep = Annotated[PaginationParams, Depends()]

class HotelParams(BaseModel):
    id: Annotated[int, Query(description="Номер страницы", ge=1)]
HotelDep = Annotated[HotelParams, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Нет токена доступа")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_current_user_id)]
