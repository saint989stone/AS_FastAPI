from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select

router = APIRouter(prefix="/hotels", tags=["hotels"])

#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@router.get("/")
def func():
    return "Hello FastAPI"

@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description="ID"),
        title: str | None = Query(default=None, description="Название"),
        location: str | None = Query(default=None, description="Расположение"),
):
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter(HotelsORM.title.ilike('%' + title + '%'))
        if location:
            query = query.filter(HotelsORM.location.ilike('%' + location + '%'))
        query = (
            query
            .limit(pagination.per_page)         #количество записей на одной страницы
            .offset(pagination.per_page * (pagination.page - 1))         #сдвиг записей на странице, то есть скакой записи начинается страница
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
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
        stmt = insert(HotelsORM).values(**data.model_dump())
        print(engine, stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(stmt)
        await session.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление об отелях",
    description="Можно обновить один атрибут"
)
def patch_hotel(
        hotel_id: int,
        data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if data.title and hotel["title"] != data.title:
                hotel["title"] = data.title
            if data.name and hotel["name"] != data.name:
                hotel["name"] = data.name
            return {"status": "OK"}
        else:
            continue


@router.put("/{hotel_id}")
def put_hotel(
        hotel_id: int,
        data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = data.title
            hotel["name"] = data.name
            return {"status": "OK"}
        else:
            continue