from fastapi import Query, Body, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["hotels"])

class Hotel(BaseModel):
    title: str
    name: str

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Santa", "name": "santa"},
]
#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@router.get("/")
def func():
    return "Hello FastAPI"

@router.get("")
def get_hotels(
        id: int | None = Query(default=None, description="ID записи"),
        title: str | None = Query(default=None, description="Назание отеля")
):
    hotels_list = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_list.append(hotel)
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
def create_hotel(data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": data.title,
        "name": data.name,
    })

@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление об отелях",
    description="Можно обновить один атрибут"
)
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(embed=True, default=None),
        name: str | None = Body(embed=True, default=None),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title and hotel["title"] != title:
                hotel["title"] = title
            if name and hotel["name"] != name:
                hotel["name"] = name
            return {"status": "200"}
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
            return {"status": 200}
        else:
            continue