from fastapi import APIRouter, Depends, HTTPException
from services.director import (
    create_director_service,
    get_director_by_id_service,
    get_all_directors_service,
    update_director_service,
    get_movies_for_director_service,
    delete_director_service
)

from models.director import DirectorCreate, DirectorResponse, DirectorUpdate
from models.movie import MovieResponse
from helper import get_current_user, admin_required
router = APIRouter(prefix="/directors", tags=["Directors"])

@router.post("/", response_model=DirectorResponse)
def create_director(director: DirectorCreate, current_user: dict = Depends(admin_required)):
    return create_director_service(director)

@router.get("/{director_id}/", response_model=DirectorResponse)
def get_director_by_id(director_id: int, current_user: dict = Depends(get_current_user)):
    return get_director_by_id_service(director_id)

@router.get("/", response_model=list[DirectorResponse])
def get_all_directors( current_user: dict = Depends(get_current_user)):
    return get_all_directors_service()

@router.put("/{director_id}/", response_model=DirectorResponse)
def update_director(director_id: int, director_update: DirectorUpdate, current_user: dict = Depends(admin_required)):
    return update_director_service(director_id, director_update)

@router.get("/{director_id}/movies", response_model=list[MovieResponse])
def get_movies_for_director(director_id: int, current_user: dict = Depends(get_current_user)):
    return get_movies_for_director_service(director_id)


@router.delete("/{director_id}/", response_model=dict)
def delete_director(director_id: int,current_user: dict = Depends(admin_required)):
    return delete_director_service(director_id)