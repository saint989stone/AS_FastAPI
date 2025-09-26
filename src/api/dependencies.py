from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=2, description="Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(default=3, description="Количество элементов на странице", ge=1, le=30)]

PaginationDep = Annotated[PaginationParams, Depends()]