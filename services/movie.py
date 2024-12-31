from models.movie import MovieResponse, MovieDetailResponse, ReviewCreate, ReviewResponse,  ReviewResponse2, CreateMovie
from crud.movie import fetch_all_movies, fetch_movie_by_id, insert_review, fetch_reviews, delete_review_from_db
from crud.movie import add_movie_to_db, add_actors_to_movie, add_genres_to_movie, add_awards_to_movie, update_movie_in_db, delete_movie_from_db
from fastapi import HTTPException, status


def get_all_movies_service() -> list[MovieResponse]:
    movies = fetch_all_movies()
    try:
        return [MovieResponse(**movie) for movie in movies]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movies not found"
        )


def get_movie_by_id_service(movie_id: int) -> MovieDetailResponse:
    try:
        # Film verilerini getir
        data = fetch_movie_by_id(movie_id)

        # Film bulunamazsa kontrol
        if not data or not data.get("movie"):
            raise ValueError("Movie not found")

        # Gelen veriyi işleyip model formatına dönüştür
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

    except ValueError as e:
        # Eğer film bulunamazsa 404 hatası döndür
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        # Diğer beklenmeyen hatalar için genel bir 500 yanıtı döndür
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_reviews_service(movie_id: int) -> list[ReviewResponse2]:
    try:
        reviews = fetch_reviews(movie_id)

        if not reviews:
            raise ValueError("No reviews found for the given movie.")

        return [ReviewResponse2(**review) for review in reviews]

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    



def add_review_service(user_id: int, movie_id: int, review: ReviewCreate) -> ReviewResponse:
    try:
        result = insert_review(user_id, movie_id, review.content, review.rating)
        if not result:
            raise ValueError("Review could not be added")
        

        # ReviewResponse formatına dönüştür             BU KISIM ÖNEMLİ DÖNÜŞTÜRME İŞLEMİ YAPILMALI RESPONSE İÇİN
        return ReviewResponse(
            review_id=result["review_id"],
            movie_id=result["movie_id"],
            user_id=result["user_id"],
            content=result["content"],
            rating=result["rating"],
            created_at=result["created_at"]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


def delete_review_service(user_id:int, review_id: int) -> ReviewResponse:
    try:
        result = delete_review_from_db(user_id, review_id)
        if not result:
            raise ValueError("Review could not be deleted")

        return ReviewResponse(
            review_id=result["review_id"],
            movie_id=result["movie_id"],
            user_id=result["user_id"],
            content=result["content"],
            rating=result["rating"],
            created_at=result["created_at"]
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")






def add_movie_service(movie_data: CreateMovie) -> MovieDetailResponse:
    try:
        movie_id = add_movie_to_db(movie_data.title, movie_data.release_year, movie_data.director_id)

        if movie_data.actor_ids:
            add_actors_to_movie(movie_id, movie_data.actor_ids)
        if movie_data.genre_ids:
            add_genres_to_movie(movie_id, movie_data.genre_ids)
        if movie_data.award_ids:
            add_awards_to_movie(movie_id, movie_data.award_ids),
        
        data = fetch_movie_by_id(movie_id)
        if not data:
            raise ValueError("Movie not found")

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
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")





def update_movie_service(movie_id:int, movie:CreateMovie) -> MovieDetailResponse:     
    try:
        update_movie_in_db(movie_id, movie.title, movie.release_year, movie.director_id)

        data = fetch_movie_by_id(movie_id)
        if not data:
            raise ValueError("Movie not found")
        
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
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def delete_movie_service(movie_id:int) -> MovieDetailResponse:  
    try:
        data = fetch_movie_by_id(movie_id)
        if not data:
            raise ValueError("Movie not found")
        
        delete_movie_from_db(movie_id)
        
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
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")