from typing import List
from fastapi import APIRouter, Depends
from models.watchlist import WatchlistResponse, WatchlistCreate
from models.movie import MovieResponse
from services.watchlist import create_watchlist_service,get_movies_in_watchlist_service, add_movie_to_watchlist_service, remove_movie_from_watchlist_service
from services.watchlist import get_movies_in_watchlist_service,delete_watchlist_service, update_watchlist_service, get_watchlists_service
from helper import get_current_user

router = APIRouter(
    prefix = "/wathlist",
    tags = ["Watchlist"]
)

@router.post("/", response_model=WatchlistResponse)
def create_watchlist(watchlist: WatchlistCreate, current_user: dict = Depends(get_current_user)):
    return create_watchlist_service(current_user["user_id"], watchlist)

@router.put("/", response_model=WatchlistResponse)
def update_watchlist(watchlist_id: int, watchlist: WatchlistCreate, current_user: dict = Depends(get_current_user)):
    return update_watchlist_service(watchlist_id, watchlist, current_user["user_id"])

@router.delete("/", response_model=WatchlistResponse)
def delete_watchlist(watchlist_id: int, current_user: dict = Depends(get_current_user)):
    return delete_watchlist_service(watchlist_id, current_user["user_id"])

@router.get("/{user_id}/", response_model=List[WatchlistResponse])
def get_watchlists(user_id:int, current_user: dict = Depends(get_current_user)):    #user_id tokenden alınmıyor, çünkü herkesin watchlistlerini görmek isteyebiliriz.
    return get_watchlists_service(user_id)


@router.get("/{watchlist_id}/movies/", response_model=List[MovieResponse])
def get_movies_in_watchlist(watchlist_id: int, current_user: dict = Depends(get_current_user)):
    return get_movies_in_watchlist_service(watchlist_id)







@router.post("/{watchlist_id}/movies/", response_model=MovieResponse)  
def add_movie_to_watchlist(watchlist_id: int, movie_id:int, current_user: dict = Depends(get_current_user)):
    return add_movie_to_watchlist_service(watchlist_id, movie_id, current_user["user_id"])




@router.delete("/{watchlist_id}/movies/{movie_id}/", response_model=MovieResponse)   #Responsemodel güncellenmeli
def remove_movie_from_watchlist(watchlist_id: int, movie_id:int, current_user: dict = Depends(get_current_user)):
    return remove_movie_from_watchlist_service(watchlist_id, movie_id, current_user["user_id"])

@router.get("/{watchlist_id}/movies/", response_model=List[MovieResponse])
def get_movies_in_watchlist(watchlist_id: int, current_user: dict = Depends(get_current_user)):
    return get_movies_in_watchlist_service(watchlist_id)