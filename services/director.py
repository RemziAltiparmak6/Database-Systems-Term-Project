from crud.director import insert_director, fetch_director_by_id, fetch_all_directors, update_director, get_movies_for_director,delete_director
from models.director import DirectorCreate, DirectorResponse, DirectorUpdate
from models.movie import MovieResponse
from fastapi import HTTPException, status
from typing import List

def create_director_service(director: DirectorCreate) -> DirectorResponse:
    """
    Creates a new director.
    """
    try:
        # Call the CRUD operation to insert the director and get the director ID
        director_id = insert_director(director)
        
        # Return the director response
        return DirectorResponse(
            director_id=director_id,
            name=director.name,
            nationality=director.nationality,
            birth_year=director.birth_year
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the director: {str(e)}"
        )

def get_director_by_id_service(director_id: int) -> DirectorResponse:
    """
    Retrieves a director by their ID.
    """
    director = fetch_director_by_id(director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Director with ID {director_id} not found."
        )
    
    # Return the director details using the DirectorResponse model
    return DirectorResponse(**director)  # Unpack the dictionary or tuple returned by the CRUD function

def get_all_directors_service() -> List[DirectorResponse]:
    """
    Retrieves all directors.
    """
    try:
        directors = fetch_all_directors()
        if not directors:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No directors found."
            )
        
        # Return the list of directors formatted as DirectorResponse models
        return [DirectorResponse(**director) for director in directors]  # Unpack each director dictionary or tuple into DirectorResponse
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching directors: {str(e)}"
        )

def update_director_service(director_id: int, director_update: DirectorUpdate) -> DirectorResponse:
    """
    Updates a director's details.
    """
    director = fetch_director_by_id(director_id)
    if not director:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Director with ID {director_id} not found."
        )

    try:
        updated_director_id = update_director(director_id, director_update.dict(exclude_unset=True))  # Ensure only updated fields
        updated_director = fetch_director_by_id(updated_director_id)
        if not updated_director:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Director with ID {director_id} not found after update."
            )
        
        return DirectorResponse(**updated_director)  # Unpack the updated director data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the director: {str(e)}"
        )

def get_movies_for_director_service(director_id: int) -> List[MovieResponse]:
    """
    Retrieves all movies for a specific director.
    """
    try:
        movies = get_movies_for_director(director_id)
        
        if not movies:
            # If no movies are found, return an empty list
            return []  # No movies found, so return an empty list
        
        movie_responses = [MovieResponse(
            movie_id=movie[0],  
            title=movie[1],
            release_year=movie[2],
            director_name=movie[3]
        ) for movie in movies]  
        
        return movie_responses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching movies for director: {str(e)}"
        )



def delete_director_service(director_id: int):
    """
    Deletes a director.
    """
    try:
        delete_director(director_id)
        return {"message": f"Director with ID {director_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the director: {str(e)}"
        )