from models.movie import MovieResponse, MovieDetailResponse, ReviewCreate, ReviewResponse,  ReviewResponse2
from crud.movie import fetch_all_movies, fetch_movie_by_id, insert_review, fetch_reviews


def get_all_movies_service() -> list[MovieResponse]:
    movies = fetch_all_movies()
    return [MovieResponse(**movie) for movie in movies]


def get_movie_by_id_service(movie_id: int) -> MovieDetailResponse:
    data =  fetch_movie_by_id(movie_id)
    movie_data = {
        "movie_id": data["movie"][0],
        "title": data["movie"][1],
        "release_year": data["movie"][2],
        "director_name": data["movie"][3],
        "genres": [{"genre_id": g[0], "name": g[1]} for g in data["genres"]],
        "actors": [
            {"actor_id": a[0], "name": a[1], "birth_year": a[2], "nationality": a[3]}
            for a in data["actors"]
        ],
        "awards": [{"award_id": a[0], "name": a[1], "year": a[2]} for a in data["awards"]]
    }
    return MovieDetailResponse(**movie_data)


def add_review_service(movie_id: int, review_data: ReviewCreate) -> ReviewResponse:
    """
    Bir Movie'ye Review ekler ve yanıt olarak ReviewResponse döner.
    """
    review = insert_review(
        movie_id=movie_id,
        user_id=review_data.user_id,
        content=review_data.content,
        rating=review_data.rating
    )
    # ReviewResponse formatına dönüştür
    return ReviewResponse(
        review_id=review[0],
        movie_id=review[1],
        user_id=review[2],
        content=review[3],
        rating=review[4],
        created_at=review[5]
    )

def get_reviews_service(movie_id: int) -> list[ReviewResponse2]:
    """
    Bir film için tüm yorumları getirir.
    """
    reviews = fetch_reviews(movie_id)
    return [ReviewResponse2(**review) for review in reviews]