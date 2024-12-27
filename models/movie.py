from pydantic import BaseModel
from typing import Optional
from datetime import date

# Movie Response Model (for GET requests)
class MovieResponse(BaseModel):
    movie_id: int
    title: str
    original_language: Optional[str] = None
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    overview: Optional[str] = None
    director_id: Optional[int] = None  # Foreign key reference to director

    class Config:
        orm_mode = True  # Tells Pydantic to treat this like a SQLAlchemy model


# Movie Create Model (for POST/PUT requests)
class MovieCreate(BaseModel):
    title: str
    original_language: Optional[str] = None
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    overview: Optional[str] = None
    director_id: Optional[int] = None  # Foreign key reference to director

    class Config:
        orm_mode = True  # Allows conversion between ORM and Pydantic models

# Movie Update Model (for updating existing movie data)
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    original_language: Optional[str] = None
    release_date: Optional[date] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    overview: Optional[str] = None
    director_id: Optional[int] = None  # Foreign key reference to director

    class Config:
        orm_mode = True  # Allows conversion between ORM and Pydantic models
