from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, HotelDep, DBDep
from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.repositories.hotels import HotelsRepo
from datetime import date

router = APIRouter(prefix="/hotels", tags=["Отели"])

#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@router.get("/")
def func():
    return "Hello FastAPI"

@router.get("")
@cache(expire=10)
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(default=None, descriptiendon="Название"),
        location: str | None = Query(default=None, description="Расположение"),
):
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )

@router.get("/bookings")
async def get_hotels_bookings(
        db: DBDep,
        pagination: PaginationDep,
        title: str | None = Query(default=None, descriptiendon="Название"),
        location: str | None = Query(default=None, description="Расположение"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.hotels.get_filtred_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel(db: DBDep, hotel: HotelDep):
    return await db.hotels.get_one_or_none(id=hotel.id)

@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int,
        db: DBDep
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}

#в запросах запросах post, put, patch параметры принимаются в теле запроса
@router.post("")
async def create_hotel(db: DBDep, data: HotelAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Сочи",
            "value": {
                "title": "Lastochka",
                "location": "г. Сочи, ул. Моря 1",
            },
        },
        "2": {
            "summary": "Дубай",
            "value": {
                "title": "Resot 5 Stars",
                "location": "г. Дубай, ул. Шейха 2",
            },
        },
    })
):
    hotel = await db.hotels.add(data)
    await db.commit()
    return {"status": "OK", "data": hotel}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление об отелях",
    description="Можно обновить один атрибут"
)
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelPATCH
):
    await db.hotels.edit(data=data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(
        db: DBDep,
        hotel_id: int,
        data: HotelAdd = Body
):
    await db.hotels.edit(data=data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}