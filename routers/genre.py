from fastapi import APIRouter
from services.genre import create_genre_service, update_genre_service, delete_genre_service, get_all_genres_service
from models.genre import GenreCreate, GenreResponse, GenreUpdate

router = APIRouter()

@router.post("/genres/", response_model=GenreResponse)
def create_genre(genre: GenreCreate):
    return create_genre_service(genre)

@router.put("/genres/{genre_id}/", response_model=dict)
def update_genre(genre_id: int, genre_update: GenreUpdate):
    return update_genre_service(genre_id, genre_update)

@router.delete("/genres/{genre_id}/", response_model=dict)
def delete_genre(genre_id: int):
    return delete_genre_service(genre_id)

@router.get("/genres/", response_model=list[GenreResponse])
def get_all_genres():
    return get_all_genres_service()
