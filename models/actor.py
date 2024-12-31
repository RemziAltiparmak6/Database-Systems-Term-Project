from pydantic import BaseModel
from typing import Optional


class ActorCreate(BaseModel):
    name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None


class ActorResponse(BaseModel):
    actor_id: int
    name: str
    birth_year: Optional[int] = None
    nationality: Optional[str] = None


class ActorUpdate(BaseModel):
    name: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None