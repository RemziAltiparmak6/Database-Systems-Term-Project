from models.director import DirectorCreate, DirectorResponse, DirectorUpdate
from crud.director import insert_director, fetch_director_by_id, fetch_all_directors, update_director
from typing import List
from fastapi import HTTPException, status


def create_director_service(director: DirectorCreate) -> DirectorResponse:
    """
    Creates a new director.
    """
    try:
        director_id = insert_director(director)
        return DirectorResponse(
            director_id=director_id,
            name=director.name,
            biography=director.biography,
            birth_date=director.birth_date,
            place_of_birth=director.place_of_birth,
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
    return DirectorResponse(**director)


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
        return [DirectorResponse(**director) for director in directors]
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
        updated_director_id = update_director(director_id, director_update.dict(exclude_unset=True))
        updated_director = fetch_director_by_id(updated_director_id)
        if not updated_director:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Director with ID {director_id} not found after update."
            )
        return DirectorResponse(**updated_director)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the director: {str(e)}"
        )



