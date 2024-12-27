from models.watchlist import WatchlistResponse, WatchlistCreate
from models.movie import MovieResponse
from datetime import datetime
from crud.watchlist import insert_watchlist, fetch_movies_in_watchlist, add_movie_to_watchlist, remove_movie_from_watchlist
from typing import List

def create_watchlist_service(user_id: int, watchlist: WatchlistCreate) -> WatchlistResponse:
    watchlist_result = insert_watchlist(user_id, watchlist.name)
    return WatchlistResponse(**watchlist_result)


def get_movies_in_watchlist_service(watchlist_id: int) -> List[MovieResponse]:
    movies = fetch_movies_in_watchlist(watchlist_id)
    return [MovieResponse(**movie) for movie in movies]

def add_movie_to_watchlist_service(watchlist_id: int, movie_id: int, user_id :int) -> List[MovieResponse]:
    results = add_movie_to_watchlist(watchlist_id, movie_id, user_id)
    return [MovieResponse(**result) for result in results]

def remove_movie_from_watchlist_service(watchlist_id: int, movie_id: int, user_id: int) -> List[MovieResponse]:
    results = remove_movie_from_watchlist(watchlist_id, movie_id, user_id)
    return [MovieResponse(**result) for result in results]

def get_movies_in_watchlist_service(watchlist_id: int) -> List[MovieResponse]:
    movies = fetch_movies_in_watchlist(watchlist_id)
    return [MovieResponse(**movie) for movie in movies]
