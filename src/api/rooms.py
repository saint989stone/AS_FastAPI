from datetime import date

from fastapi import APIRouter, Body, Query

from src.schemas.facilities import RoomFacilityAdd
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
    _data = RoomAdd(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    room = await db.rooms.add(_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=facility_id) for facility_id in data.facilities_ids]

    await db.rooms_facilities.add_bulk(data=rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}

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
    _data_dict = data.model_dump(exclude_unset=True)
    _data = RoomPatch(hotel_id=hotel_id, **_data_dict)
    await db.rooms.edit(data=_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=_data_dict["facilities_ids"])
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
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities=data.facilities_ids)
    await db.commit()
    return {"status": "OK"}