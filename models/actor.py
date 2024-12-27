from pydantic import BaseModel
from typing import Optional
from datetime import date

class ActorCreate(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None


class ActorResponse(BaseModel):
    actor_id: int
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None


class ActorUpdate(BaseModel):
    name: Optional[str] = None
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    place_of_birth: Optional[str] = None