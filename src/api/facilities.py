from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep, HotelDep, DBDep
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(db: DBDep, data: FacilityAdd = Body(
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
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}