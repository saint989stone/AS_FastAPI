from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, HotelDep
from src.database import async_session_maker, engine
from src.schemas.hotels import Hotel, HotelPATCH
from src.repositories.hotels import HotelsRepo

router = APIRouter(prefix="/hotels", tags=["hotels"])

#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@router.get("/")
def func():
    return "Hello FastAPI"

@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(default=None, description="Название"),
        location: str | None = Query(default=None, description="Расположение"),
):
    async with async_session_maker() as session:
        return await HotelsRepo(session).get_all(
            title=title,
            location=location,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )

@router.get("/{hotel_id}")
async def get_hotel(hotel: HotelDep):
    async with async_session_maker() as session:
        return await HotelsRepo(session).get_one_or_none(id=hotel.id)

@router.delete("/{hotel_id}")
async def delete_hotel(
        hotel_id: int
):
    async with async_session_maker() as session:
        await HotelsRepo(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}

#в запросах запросах post, put, patch параметры принимаются в теле запроса
@router.post("")
async def create_hotel(data: Hotel = Body(
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
    async with async_session_maker() as session:
        hotel = await HotelsRepo(session).add(data)
        await session.commit()
    return {"status": "OK", "data": hotel}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление об отелях",
    description="Можно обновить один атрибут"
)
async def patch_hotel(
        hotel_id: int,
        data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepo(session).edit(data=data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(
        hotel_id: int,
        data: Hotel = Body
):
    async with async_session_maker() as session:
        await HotelsRepo(session).edit(data=data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}