from db import get_db
from datetime import datetime



#bunlarda rollback yok

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
    


def fetch_reviews(movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT r.review_id, r.user_id, u.username, r.content, r.rating, r.created_at
            FROM user_review r
            JOIN "user" u ON r.user_id = u.user_id
            WHERE r.movie_id = %s;
        """
        cursor.execute(query, (movie_id,))
        rows = cursor.fetchall()
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
    




def insert_review(user_id: int, movie_id: int, content: str, rating: float):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO user_review (user_id, movie_id, content, rating, created_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING review_id, user_id, movie_id, content, rating, created_at;
            """
            cursor.execute(query, (user_id, movie_id, content, rating))
            conn.commit()
            row = cursor.fetchone()

            return {
                "review_id": row[0],
                "user_id": row[1],
                "movie_id": row[2],
                "content": row[3],
                "rating": row[4],
                "created_at": row[5].isoformat() if isinstance(row[5], datetime) else row[5]
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while adding review: {str(e)}")

    

    
def delete_review_from_db(user_id: int, review_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                DELETE FROM user_review
                WHERE review_id = %s AND user_id = %s
                RETURNING review_id, user_id, movie_id, content, rating, created_at;
            """
            cursor.execute(query, (review_id, user_id))
            result = cursor.fetchone()
            conn.commit()

            return {
                "review_id": result[0],
                "user_id": result[1],
                "movie_id": result[2],
                "content": result[3],
                "rating": result[4],
                "created_at": result[5].isoformat() if isinstance(result[5], datetime) else result[5]
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while deleting review: {str(e)}")
    








def add_movie_to_db(title: str, release_year: int, director_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO movie (title, release_year, director_id)
                VALUES (%s, %s, %s)
                RETURNING movie_id;
            """
            cursor.execute(query, (title, release_year, director_id))
            movie_id = cursor.fetchone()[0]
            conn.commit()
            return movie_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while adding movie: {str(e)}")
        
        
        

def add_actors_to_movie(movie_id: int, actor_ids: list[int]):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO movie_actor (movie_id, actor_id)
                VALUES (%s, %s);
            """
            for actor_id in actor_ids:
                cursor.execute(query, (movie_id, actor_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while adding actors: {str(e)}")


def add_genres_to_movie(movie_id: int, genre_ids: list[int]):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO movie_genre (movie_id, genre_id)
                VALUES (%s, %s);
            """
            for genre_id in genre_ids:
                cursor.execute(query, (movie_id, genre_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while adding genres: {str(e)}")



def add_awards_to_movie(movie_id: int, award_ids: list[int]):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO movie_award (movie_id, award_id)
                VALUES (%s, %s);
            """
            for award_id in award_ids:
                cursor.execute(query, (movie_id, award_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while adding awards: {str(e)}")
        


def update_movie_in_db(movie_id: int, title: str = None, release_year: int = None, director_id: int = None):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            if title:
                cursor.execute("UPDATE movie SET title = %s WHERE movie_id = %s;", (title, movie_id))
            if release_year:
                cursor.execute("UPDATE movie SET release_year = %s WHERE movie_id = %s;", (release_year, movie_id))
            if director_id:
                cursor.execute("UPDATE movie SET director_id = %s WHERE movie_id = %s;", (director_id, movie_id))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while updating movie: {str(e)}")






def delete_movie_from_db(movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM movie WHERE movie_id = %s RETURNING movie_id;"
            cursor.execute(query, (movie_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Movie not found")
            conn.commit()
            return row[0]
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error while deleting movie: {str(e)}")



