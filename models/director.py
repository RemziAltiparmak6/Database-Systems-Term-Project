from pydantic import BaseModel
from typing import Optional
from datetime import date

class DirectorCreate(BaseModel):
    name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None


class DirectorResponse(BaseModel):
    director_id: int
    name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None

    class Config:
        orm_mode = True


class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
