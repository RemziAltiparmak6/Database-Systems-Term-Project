from fastapi import APIRouter
from models.actor import ActorCreate, ActorResponse, ActorUpdate
from models.movie import MovieResponse
from services.actor import (
    create_actor_service,
    get_actor_by_id_service,
    get_all_actors_service,
    update_actor_service,
    get_movies_for_actor_service
)

router = APIRouter(prefix="/actors", tags=["Actors"])

@router.post("/", response_model=ActorResponse)
def create_actor(actor: ActorCreate):
    return create_actor_service(actor)


@router.get("/{actor_id}/", response_model=ActorResponse)
def get_actor_by_id(actor_id: int):
    return get_actor_by_id_service(actor_id)


@router.get("/", response_model=list[ActorResponse])
def get_all_actors():
    return get_all_actors_service()


@router.put("/{actor_id}/", response_model=ActorResponse)
def update_actor(actor_id: int, actor_update: ActorUpdate):
    return update_actor_service(actor_id, actor_update)


# Endpoint to get all movies for a specific actor
@router.get("/{actor_id}/movies", response_model=list[MovieResponse])
def get_movies_for_actor(actor_id: int):
    
    # Call the service to get all movies for the actor
    return get_movies_for_actor_service(actor_id)
