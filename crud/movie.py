from db import get_db
from datetime import datetime

def fetch_all_movies():
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT m.movie_id, m.title, m.release_year, d.name AS director_name
            FROM movie m
            JOIN director d ON m.director_id = d.director_id;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        # Veriyi dönüştürüp döndür
        return [
            {
                "movie_id": row[0],
                "title": row[1],
                "release_year": row[2],
                "director_name": row[3]
            }
            for row in rows
        ]
    

def fetch_movie_by_id(movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()

        # Film bilgileri ve yönetmen
        movie_query = """
            SELECT m.movie_id, m.title, m.release_year, d.name AS director_name
            FROM movie m
            JOIN director d ON m.director_id = d.director_id
            WHERE m.movie_id = %s;
        """
        cursor.execute(movie_query, (movie_id,))
        movie = cursor.fetchone()

        # Türler
        genres_query = """
            SELECT g.genre_id, g.name
            FROM genre g
            JOIN movie_genre mg ON g.genre_id = mg.genre_id
            WHERE mg.movie_id = %s;
        """
        cursor.execute(genres_query, (movie_id,))
        genres = cursor.fetchall()

        # Oyuncular
        actors_query = """
            SELECT a.actor_id, a.name, a.birth_year, a.nationality
            FROM actor a
            JOIN movie_actor ma ON a.actor_id = ma.actor_id
            WHERE ma.movie_id = %s;
        """
        cursor.execute(actors_query, (movie_id,))
        actors = cursor.fetchall()

        # Ödüller
        awards_query = """
            SELECT a.award_id, a.name, a.year
            FROM award a
            JOIN movie_award ma ON a.award_id = ma.award_id
            WHERE ma.movie_id = %s;
        """
        cursor.execute(awards_query, (movie_id,))
        awards = cursor.fetchall()

        return {
            "movie": movie,
            "genres": genres,
            "actors": actors,
            "awards": awards
        }



def insert_review(movie_id: int, user_id: int, content: str, rating: float):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO user_review (movie_id, user_id, content, rating, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING review_id, movie_id, user_id, content, rating, created_at;
        """
        cursor.execute(query, (movie_id, user_id, content, rating))
        conn.commit()
        return cursor.fetchone()
    

def fetch_reviews(movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT r.review_id, r.user_id, u.username, r.content, r.rating, r.created_at
            FROM user_review r
            JOIN user u ON r.user_id = u.user_id
            WHERE r.movie_id = %s;
        """
        cursor.execute(query, (movie_id,))
        rows = cursor.fetchall()
        # Veriyi dönüştürüp döndür
        return [
            {
                "review_id": row[0],
                "user_id": row[1],
                "username": row[2],
                "content": row[3],
                "rating": row[4],
                "created_at": row[5].isoformat() if isinstance(row[5], datetime) else row[5]

            }
            for row in rows
        ]