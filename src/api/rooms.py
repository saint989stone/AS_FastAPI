from datetime import date

from fastapi import APIRouter, Body, Query
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtred_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(db: DBDep, hotel_id: int, room_id: int,):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

#в запросах запросах post, put, patch параметры принимаются в теле запроса
@router.post("/{hotel_id}/rooms")
async def create_room(db: DBDep, hotel_id: int, data: RoomAddRequest = Body()):
    _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.add(data=_data)
    await db.commit()
    return {"status": "OK"}

@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление информации о номерах",
    description="Можно обновить один атрибут"
)
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequest
):
    _data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomAddRequest = Body
):
    _data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(data=_data, id=room_id)
    await db.commit()
    return {"status": "OK"}