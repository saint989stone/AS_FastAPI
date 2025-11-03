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
    _data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    db_facilities_ids = await db.rooms_facilities.get_all(room_id=room_id)
    set_db_facilities_ids = {room_facility.facility_id for room_facility in db_facilities_ids}
    set_user_facilities_ids = set(data.facilities_ids)
    print(set_db_facilities_ids)
    print(set_user_facilities_ids)
    set_add_facilities_ids = set_user_facilities_ids - set_db_facilities_ids
    set_del_facilities_ids = set_db_facilities_ids - set_user_facilities_ids
    room_facilities_data = [RoomFacilityAdd(room_id=room_id, facility_id=facility_id) for facility_id in set_add_facilities_ids]
    if set_add_facilities_ids:
        await db.rooms_facilities.add_bulk(data=room_facilities_data)
    # if set_del_facilities_ids:
    #     await db.rooms_facilities.delete_bulk(room_facilities_data)
    await db.commit()
    # await db.rooms.edit(data=data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    # await db.commit()
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