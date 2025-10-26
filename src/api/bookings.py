from fastapi import Query, APIRouter, Body, Request
from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("/{room_id}/bookings")
async def create_booking(db: DBDep, room_id: int ,request: Request, data: BookingAddRequest = Body(
    openapi_examples={
        "1": {
            "summary": "booking#1",
            "value": {
                "date_from": "2021-01-01",
                "date_to": "2021-01-02",
            },
        },
        "2": {
            "summary": "bookings#2",
            "value": {
                "date_from": "01.01.2021",
                "date_to": "02.01.2021",
            },
        },
    })
):
    room = await db.rooms.get_one_or_none(id=room_id)
    access_token = request.cookies.get("access_token")
    decode_token = AuthService().decode_token(access_token)
    user_id = decode_token["user_id"]
    _data = BookingAdd(user_id=user_id, room_id=room_id, price=room.price, **data.model_dump())
    await db.bookings.add(_data)
    await db.commit()
    return {"status": "OK", "room": room}