from pydantic import BaseModel
from typing import Optional


# Movie Response Model (for GET requests)
class MovieResponse(BaseModel):
    movie_id: int
    title: str
    director_id: Optional[int] = None  # Foreign key reference to director
    release_year: Optional[int] = None
    class Config:
        orm_mode = True  # Tells Pydantic to treat this like a SQLAlchemy model


# Movie Create Model (for POST/PUT requests)
class MovieCreate(BaseModel):
    title: str
    director_id: Optional[int] = None  # Foreign key reference to director
    release_year: Optional[int] = None

    class Config:
        orm_mode = True  # Allows conversion between ORM and Pydantic models

# Movie Update Model (for updating existing movie data)
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director_id: Optional[int] = None  # Foreign key reference to director
    release_year: Optional[int] = None

    class Config:
        orm_mode = True  # Allows conversion between ORM and Pydantic models



from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class GenreResponse(BaseModel):
    genre_id: int
    name: str


class AwardResponse(BaseModel):
    award_id: int
    name: str
    year: int

class AwardCreate(BaseModel):
    name: str
    year: int
    
    
class GenreCreate(BaseModel):
    name: str
    
    
class ActorUpdate(BaseModel):
    name: Optional[str] = None
    birth_year: Optional[int] = None
    nationality: Optional[str] = None