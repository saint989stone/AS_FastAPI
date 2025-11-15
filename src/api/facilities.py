from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache
import json

from src.api.dependencies import PaginationDep, HotelDep, DBDep
from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("Иду в БД")
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(db: DBDep, data: FacilityAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Internet",
            "value": {
                "title": "Internet",
            },
        },
        "2": {
            "summary": "Сonditioner",
            "value": {
                "title": "Сonditioner",
            },
        },
    })
):
    facility = await db.facilities.add(data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}