from models.actor import ActorCreate, ActorResponse, ActorUpdate
from crud.actor import insert_actor, fetch_actor_by_id, fetch_all_actors, update_actor
from typing import List
from fastapi import HTTPException, status


def create_actor_service(actor: ActorCreate) -> ActorResponse:
    """
    Creates a new actor.
    """
    try:
        actor_id = insert_actor(actor)
        return ActorResponse(
            actor_id=actor_id,
            name=actor.name,
            biography=actor.biography,
            birth_date=actor.birth_date,
            place_of_birth=actor.place_of_birth,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the actor: {str(e)}"
        )


def get_actor_by_id_service(actor_id: int) -> ActorResponse:
    """
    Retrieves an actor by their ID.
    """
    actor = fetch_actor_by_id(actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Actor with ID {actor_id} not found."
        )
    return ActorResponse(**actor)


def get_all_actors_service() -> List[ActorResponse]:
    """
    Retrieves all actors.
    """
    try:
        actors = fetch_all_actors()
        if not actors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No actors found."
            )
        return [ActorResponse(**actor) for actor in actors]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching actors: {str(e)}"
        )


def update_actor_service(actor_id: int, actor_update: ActorUpdate) -> ActorResponse:
    """
    Updates an actor's details.
    """
    actor = fetch_actor_by_id(actor_id)
    if not actor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Actor with ID {actor_id} not found."
        )

    try:
        updated_actor_id = update_actor(actor_id, actor_update.dict(exclude_unset=True))
        updated_actor = fetch_actor_by_id(updated_actor_id)
        if not updated_actor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Actor with ID {actor_id} not found after update."
            )
        return ActorResponse(**updated_actor)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the actor: {str(e)}"
        )


