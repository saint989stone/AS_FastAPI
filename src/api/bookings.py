from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_bookings(
        db: DBDep
):
    return await db.bookings.get_all()

@router.get("/me")
async def get_bookings_me(
        db: DBDep,
        user_id: UserIdDep
):
    return await db.bookings.get_filtered(id=user_id)

@router.post("")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        data: BookingAddRequest = Body(
    openapi_examples={
        "1": {
            "summary": "booking#1",
            "value": {
                "room_id": 8,
                "date_from": "2021-01-01",
                "date_to": "2021-01-02",
            },
        },
        "2": {
            "summary": "bookings#2",
            "value": {
                "room_id": 8,
                "date_from": "01.01.2021",
                "date_to": "02.01.2021",
            },
        },
    })
):
    room = await db.rooms.get_one_or_none(id=data.room_id)
    room_price: int = room.price
    _data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **data.model_dump())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"status": 200, "data": booking}

