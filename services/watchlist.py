from models.watchlist import WatchlistResponse, WatchlistCreate
from models.movie import MovieResponse
from datetime import datetime
from crud.watchlist import insert_watchlist, fetch_movies_in_watchlist, add_movie_to_watchlist, fetch_watchlists
from crud.watchlist import remove_movie_from_watchlist, delete_watchlist, update_watchlist, get_watchlist_owner
from typing import List
from fastapi import HTTPException


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


def create_watchlist_service(user_id: int, watchlist: WatchlistCreate) -> WatchlistResponse:
    try:
        watchlist_result = insert_watchlist(user_id, watchlist.name)
        if not watchlist_result:
            raise HTTPException(status_code=400, detail="Failed to create watchlist")
        return WatchlistResponse(**watchlist_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

    
def update_watchlist_service(watchlist_id: int, watchlist: WatchlistCreate, user_id: int) -> WatchlistResponse:
    try:
        watchlist_owner = get_watchlist_owner(watchlist_id) 

        if watchlist_owner != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to modify this watchlist.")
        
        watchlist_result = update_watchlist(watchlist_id, watchlist.name)   #Artık user_id'nin crud katmanına gitmesine gerek yok.
        if not watchlist_result:
            raise HTTPException(status_code=404, detail="Watchlist not found")
        return WatchlistResponse(**watchlist_result)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

def delete_watchlist_service(watchlist_id: int, user_id: int) -> WatchlistResponse:
    try:
        watchlist_owner = get_watchlist_owner(watchlist_id) 

        if watchlist_owner != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to modify this watchlist.")
        
        watchlist = delete_watchlist(watchlist_id)
        if not watchlist:
            raise HTTPException(status_code=404, detail="Watchlist not found")
        return WatchlistResponse(**watchlist)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

def get_watchlists_service(user_id: int) -> List[WatchlistResponse]:    #user_id'yi tokenden gelmiyor çünkü herkesin watchlistlerini görmesine izin veriyoruz.xs
    try:
        watchlists = fetch_watchlists(user_id)
        if not watchlists:
            raise HTTPException(status_code=404, detail="Watchlists not found")
        return [WatchlistResponse(**watchlist) for watchlist in watchlists]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


def add_movie_to_watchlist_service(watchlist_id: int, movie_id: int, user_id: int) -> MovieResponse:
    try:
        watchlist_owner = get_watchlist_owner(watchlist_id) 

        if watchlist_owner != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to modify this watchlist.")
        
        result = add_movie_to_watchlist(watchlist_id, movie_id)
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to add movie to the watchlist")
        
        return MovieResponse(**result)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    



def remove_movie_from_watchlist_service(watchlist_id: int, movie_id: int, user_id: int) -> List[MovieResponse]:
    try:
        watchlist_owner = get_watchlist_owner(watchlist_id) 

        if watchlist_owner != user_id:
            raise HTTPException(status_code=403, detail="You are not allowed to modify this watchlist.")
        
        results = remove_movie_from_watchlist(watchlist_id, movie_id)

        if not results:
            raise HTTPException(status_code=400, detail="Failed to remove movie from the watchlist")
        
        return [MovieResponse(**result) for result in results]
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



