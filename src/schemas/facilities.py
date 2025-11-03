from pydantic import BaseModel, Field, ConfigDict

class FacilitiesAdd(BaseModel):
    title: str

class Facilities(FacilitiesAdd):
    id: int