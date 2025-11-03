from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, HotelDep, DBDep
from src.schemas.facilities import Facilities, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(
        db: DBDep
):
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(db: DBDep, data: FacilitiesAdd = Body(
    openapi_examples={
        "1": {
            "summary": "Internet",
            "value": {
                "title": "Internet",
            },
        },
        "2": {
            "summary": "Сonditioner",
            "value": {
                "title": "Сonditioner",
            },
        },
    })
):
    facilities = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facilities}