from crud.actor import insert_actor, fetch_actor_by_id, fetch_all_actors, update_actor, get_movies_for_actor
from models.actor import ActorCreate, ActorResponse, ActorUpdate
from models.movie import MovieResponse2
from fastapi import HTTPException, status
from typing import List

def create_actor_service(actor: ActorCreate) -> ActorResponse:
    """
    Creates a new actor.
    """
    try:
        # Call the CRUD operation to insert the actor and get the actor ID
        actor_id = insert_actor(actor)
        
        # Return the actor response
        return ActorResponse(
            actor_id=actor_id,
            name=actor.name,
            birth_year=actor.birth_year,
            nationality=actor.nationality
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
    
    # Return the actor details using the ActorResponse model
    return ActorResponse(**actor)  # Unpack the dictionary or tuple returned by the CRUD function

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
        
        # Return the list of actors formatted as ActorResponse models
        return [ActorResponse(**actor) for actor in actors]  # Unpack each actor dictionary or tuple into ActorResponse
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
        updated_actor_id = update_actor(actor_id, actor_update.dict(exclude_unset=True))  # Ensure only updated fields
        updated_actor = fetch_actor_by_id(updated_actor_id)
        if not updated_actor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Actor with ID {actor_id} not found after update."
            )
        
        return ActorResponse(**updated_actor)  # Unpack the updated actor data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the actor: {str(e)}"
        )

def get_movies_for_actor_service(actor_id: int) -> List[MovieResponse2]:
    """
    Retrieves all movies for a specific actor.
    """
    try:
        # Call the CRUD function to get movies for the actor
        movies = get_movies_for_actor(actor_id)
        
        if not movies:
            # If no movies are found, return an empty list
            return []  # No movies found, so return an empty list
        
        # Format the movie data into MovieResponse model
        movie_responses = [MovieResponse2(
            movie_id=movie[0],  # Assuming movie tuple format: (movie_id, title, director_id, release_year)
            title=movie[1],
            director_id=movie[2],
            release_year=movie[3]
        ) for movie in movies]  # Convert each movie data into MovieResponse
        
        return movie_responses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching movies for actor: {str(e)}"
        )


