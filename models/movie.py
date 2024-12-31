from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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

