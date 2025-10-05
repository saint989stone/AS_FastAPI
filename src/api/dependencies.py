from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(default=5, description="Количество элементов на странице", ge=1, le=30)]

class HotelParams(BaseModel):
    id: Annotated[int, Query(description="Номер страницы", ge=1)]

PaginationDep = Annotated[PaginationParams, Depends()]
HotelDep = Annotated[HotelParams, Depends()]
