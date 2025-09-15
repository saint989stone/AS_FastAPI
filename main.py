from idlelib.query import Query

import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
    {"id": 3, "title": "Santa", "name": "santa"},
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

@app.patch("/hotels/{hotel_id}")
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


@app.put("/hotels/{hotel_id}")
def put_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": 200}
        else:
            continue

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)