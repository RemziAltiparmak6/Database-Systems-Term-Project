from crud.genre import add_genre, update_genre, delete_genre, get_all_genres
from models.genre import GenreCreate, GenreResponse, GenreUpdate
from fastapi import HTTPException, status

def create_genre_service(genre: GenreCreate) -> GenreResponse:
    """
    Creates a new genre.
    """
    try:
        genre_id = add_genre(genre)
        return GenreResponse(genre_id=genre_id, name=genre.name)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the genre: {str(e)}"
        )

def update_genre_service(genre_id: int, genre_update: GenreUpdate) -> GenreResponse:
    """
    Updates a genre's details.
    """
    try:
        updated_genre_id = update_genre(genre_id, genre_update.dict(exclude_unset=True))
        return {"genre_id": updated_genre_id,"name":genre_update.name}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the genre: {str(e)}"
        )

def delete_genre_service(genre_id: int):
    """
    Deletes a genre.
    """
    try:
        delete_genre(genre_id)
        return {"message": f"Genre with ID {genre_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the genre: {str(e)}"
        )

def get_all_genres_service():
    """
    Retrieves all genres.
    """
    try:
        genres = get_all_genres()
        return genres
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching genres: {str(e)}"
        )
