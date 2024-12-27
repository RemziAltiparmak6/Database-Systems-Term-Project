from fastapi import APIRouter
from models.director import DirectorCreate, DirectorResponse, DirectorUpdate
from services.director import (
    create_director_service,
    get_director_by_id_service,
    get_all_directors_service,
    update_director_service,
)

router = APIRouter()

@router.post("/directors/", response_model=DirectorResponse)
def create_director(director: DirectorCreate):
    return create_director_service(director)


@router.get("/directors/{director_id}/", response_model=DirectorResponse)
def get_director_by_id(director_id: int):
    return get_director_by_id_service(director_id)


@router.get("/directors/", response_model=list[DirectorResponse])
def get_all_directors():
    return get_all_directors_service()


@router.put("/directors/{director_id}/", response_model=DirectorResponse)
def update_director(director_id: int, director_update: DirectorUpdate):
    return update_director_service(director_id, director_update)
