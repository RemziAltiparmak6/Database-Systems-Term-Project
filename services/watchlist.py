from models.watchlist import WatchlistResponse, WatchlistCreate
from models.movie import MovieResponse
from datetime import datetime
from crud.watchlist import insert_watchlist, fetch_movies_in_watchlist, add_movie_to_watchlist, remove_movie_from_watchlist
from typing import List
from fastapi import HTTPException

def create_watchlist_service(user_id: int, watchlist: WatchlistCreate) -> WatchlistResponse:
    try:
        watchlist_result = insert_watchlist(user_id, watchlist.name)
        return WatchlistResponse(**watchlist_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


def get_movies_in_watchlist_service(watchlist_id: int) -> List[MovieResponse]:
    try:
        movies = fetch_movies_in_watchlist(watchlist_id)
        if not movies:
            raise HTTPException(status_code=404, detail="Movies not found in the watchlist")
        return [MovieResponse(**movie) for movie in movies]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



def add_movie_to_watchlist_service(watchlist_id: int, movie_id: int, user_id: int) -> MovieResponse:
    try:
        # Film izleme listesine eklenir ve detayları alınır
        result = add_movie_to_watchlist(watchlist_id, movie_id, user_id)
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to add movie to the watchlist")
        
        # MovieResponse formatına dönüştür
        return MovieResponse(**result)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    



def remove_movie_from_watchlist_service(watchlist_id: int, movie_id: int, user_id: int) -> List[MovieResponse]:
    try:
        results = remove_movie_from_watchlist(watchlist_id, movie_id, user_id)

        if not results:
            raise HTTPException(status_code=400, detail="Failed to remove movie from the watchlist")
        
        return [MovieResponse(**result) for result in results]
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



