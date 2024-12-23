from fastapi import APIRouter
from models.movie import MovieResponse, MovieDetailResponse, ReviewCreate, ReviewResponse, ReviewResponse2
from services.movie import get_all_movies_service, get_movie_by_id_service, add_review_service, get_reviews_service

router = APIRouter(
    prefix = "/movies",
    tags = ["Movies"]
)

@router.get("/movies/", response_model=list[MovieResponse])
def get_all_movies():
    return get_all_movies_service()


@router.get("/movies/{movie_id}", response_model=MovieDetailResponse)
def get_movie_by_id(movie_id: int):
    return get_movie_by_id_service(movie_id)


@router.post("/movies/{movie_id}/reviews/", response_model=ReviewResponse)
def add_review(movie_id: int, review: ReviewCreate):
    return add_review_service(movie_id, review)


@router.get("/movies/{movie_id}/reviews/", response_model=list[ReviewResponse2])
def get_reviews(movie_id: int):
    return get_reviews_service(movie_id)