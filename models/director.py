from pydantic import BaseModel
from typing import Optional
from datetime import date

class DirectorCreate(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None


class DirectorResponse(BaseModel):
    director_id: int
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None

    class Config:
        orm_mode = True


class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None
