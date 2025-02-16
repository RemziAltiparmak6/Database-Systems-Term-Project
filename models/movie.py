
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import Field
from typing import List


# Movie Response Model (for GET requests)
class MovieResponse2(BaseModel):
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


class MovieResponse(BaseModel):
    movie_id: int
    title: str
    release_year: int
    director_name: str


class Actor(BaseModel):
    actor_id: int
    name: str
    birth_year: Optional[int]
    nationality: Optional[str]

class Genre(BaseModel):
    genre_id: int
    name: str


class Award(BaseModel):
    award_id: int
    name: str
    year: int

class MovieDetailResponse(BaseModel):
    movie_id: int
    title: str
    release_year: int
    director_name: str
    genres: List[Genre]  # Türler
    actors: List[Actor]  # Oyuncular
    awards: List[Award]  # Ödüller


class ReviewCreate(BaseModel):
    content: str = Field(..., max_length=500)  # Maksimum uzunluk 500 karakter
    rating: float = Field(..., ge=0, le=10)  # 0 ile 10 arasında bir değer

class ReviewResponse(BaseModel):
    review_id: int
    user_id: int
    movie_id: int
    content: str
    rating: float
    created_at: datetime

class ReviewResponse2(BaseModel):
    review_id: int
    user_id: int
    username: str
    content: str
    rating: float
    created_at: datetime


class CreateMovie(BaseModel):
    title: str
    release_year: int
    director_id: int
    actor_ids: List[int]
    genre_ids: List[int]
    award_ids: List[int]


