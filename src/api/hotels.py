from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Santa", "name": "santa"},
    {"id": 4, "title": "Malg", "name": "malg"},
    {"id": 5, "title": "Shalga", "name": "shalga"},
    {"id": 6, "title": "Ney Work", "name": "ney work"},
    {"id": 7, "title": "Brons", "name": "brons"},
    {"id": 8, "title": "Kipr", "name": "kipr"},
    {"id": 9, "title": "Moscow", "name": "moscow"},
    {"id": 10, "title": "Sant-Peter", "name": "sant-peter"},
    {"id": 11, "title": "Samara", "name": "samara"},
    {"id": 12, "title": "Kazan", "name": "kazan"},
]
#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@router.get("/")
def func():
    return "Hello FastAPI"

@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(default=None, description="ID записи"),
        title: str | None = Query(default=None, description="Назание отеля"),

):
    hotels_list = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_list.append(hotel)
        if pagination.page is not None and pagination.per_page is not None:
            return hotels[(pagination.page - 1) * pagination.per_page:pagination.page * pagination.per_page]
        return hotels_list

@router.delete("/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

#в запросах запросах post, put, patch параметры принимаются в теле запроса
@router.post("")
def create_hotel(data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Sochi",
        "name": "LAstochka",
    }},
    "2": {"summary": "Dubai", "value": {
        "title": "Dubai",
        "name": "Dubai_Resot",
    }}
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": data.title,
        "name": data.name,
    })
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