from idlelib.query import Query

import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"},
    {"id": 3, "title": "Santa"}
]

#в запросах get, delete параметры принимаются из строки запроса в query параметрах
@app.get("/")
def func():
    return "Hello FastAPI"

@app.get("/hotels")
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

@app.delete("/hotels/{hotel_id}")
def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

#в запросах запросах post, put, patch параметры принимаются в теле запроса
@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),          #embed включает передачу данных в формате json
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)