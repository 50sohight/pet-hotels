from pydantic import BaseModel, Field

class Hotel(BaseModel):
    name: str
    rus_name: str

class HotelPatch(BaseModel):
    name: str | None = Field(None)
    rus_name: str | None = Field(None)