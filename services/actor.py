from models.actor import ActorCreate, ActorResponse, ActorUpdate
from models.movie import MovieResponse
from crud.actor import insert_actor, fetch_actor_by_id, fetch_all_actors, update_actor,get_movies_for_actor, get_top_movie_for_actor
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


def get_movies_for_actor_service(actor_id: int):
    """
    Retrieves all movies for a specific actor.
    """
    try:
        movies = get_movies_for_actor(actor_id)
        if not movies:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movies not found for actor"
            )
        
        # Format the movie data into MovieResponse model
        movie_responses = [MovieResponse(**movie) for movie in movies]
        return movie_responses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching movies for actor: {str(e)}"
        )

def get_top_movie_for_actor_service(actor_id: int):
    """
    Retrieves the highest-rated movie for a specific actor.
    """
    try:
        top_movie = get_top_movie_for_actor(actor_id)
        if not top_movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Top movie not found for actor"
            )
        
        # Format the top movie into MovieResponse model
        top_movie_response = MovieResponse(**top_movie)
        
        return top_movie_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching top movie for actor: {str(e)}"
        )