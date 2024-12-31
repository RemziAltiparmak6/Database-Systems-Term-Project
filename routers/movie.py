from fastapi import APIRouter, Depends, HTTPException
from models.movie import MovieResponse, MovieDetailResponse, ReviewCreate, ReviewResponse, ReviewResponse2, CreateMovie
from services.movie import get_all_movies_service, get_movie_by_id_service, add_review_service, get_reviews_service, delete_review_service
from services.movie import add_movie_service, update_movie_service, delete_movie_service
from helper import get_current_user, admin_required

router = APIRouter(
    prefix = "/movies",
    tags = ["Movies"]
)

@router.get("/", response_model=list[MovieResponse])
def get_all_movies(current_user: dict = Depends(get_current_user)):
    return get_all_movies_service()


@router.get("/{movie_id}", response_model=MovieDetailResponse)
def get_movie_by_id(movie_id: int, current_user: dict = Depends(get_current_user)):
    return get_movie_by_id_service(movie_id)







@router.post("/{movie_id}/reviews/", response_model=ReviewResponse)
def add_review(movie_id: int, review: ReviewCreate, current_user: dict = Depends(get_current_user)):
    return add_review_service(current_user["user_id"], movie_id, review)


@router.get("/{movie_id}/reviews/", response_model=list[ReviewResponse2])   # bir filmin bütün reviewlerini getirir, user_id gerek yok
def get_reviews(movie_id: int, current_user: dict = Depends(get_current_user)):
    return get_reviews_service(movie_id)


@router.delete("/reviews/{review_id}", response_model=ReviewResponse)
def delete_review(review_id:int, current_user: dict = Depends(get_current_user)):
    return delete_review_service(current_user["user_id"], review_id)









@router.post("/", response_model=MovieDetailResponse)
def add_movie(movie_data: CreateMovie, current_user: dict = Depends(admin_required)):
    return add_movie_service(movie_data)
    
    
    

@router.put("/update_movie/movie_id", response_model=MovieDetailResponse)
def update_movie(movie_id:int, movie_data: CreateMovie, current_user: dict = Depends(admin_required)):
    return update_movie_service(movie_id, movie_data)



@router.delete("/delete_movie/movie_id", response_model=MovieDetailResponse)
def delete_movie(movie_id:int, current_user: dict = Depends(admin_required)):
    return delete_movie_service(movie_id)