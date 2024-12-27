from db import get_db

    
def insert_watchlist(user_id: int, name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO watchlist (user_id, name)
                VALUES (%s, %s)
                RETURNING watchlist_id, user_id, name, created_at;
            """
            cursor.execute(query, (user_id, name))
            row = cursor.fetchone()
            conn.commit()

            return {
                "watchlist_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "created_at": row[3],
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")
        

def fetch_movies_in_watchlist(watchlist_id: int):   #Burada hata var, genre değil director name döndürmeli
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    m.movie_id, 
                    m.title, 
                    m.release_year, 
                    g.name
                FROM 
                    movies m
                JOIN 
                    movie_genre mg 
                ON 
                    m.movie_id = mg.movie_id
                JOIN
                    genre g
                On
                    mg.movie_id = g.genre_id

                WHERE 
                    wm.watchlist_id = %s;
            """
            cursor.execute(query, (watchlist_id,))
            rows = cursor.fetchall()

            return [
                {
                    "movie_id": row[0],
                    "title": row[1],
                    "release_year": row[2],
                    "director_name": row[3]
                }
                for row in rows
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        

        
def add_movie_to_watchlist(watchlist_id: int, movie_id: int, user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO watchlist_item (watchlist_id, movie_id)
                SELECT w.watchlist_id, %s
                FROM watchlist w
                WHERE w.watchlist_id = %s AND w.user_id = %s
                RETURNING watchlist_id, movie_id;
            """
            # Tüm parametreleri sağlayın
            cursor.execute(query, (movie_id, watchlist_id, user_id))
            row = cursor.fetchone()
            
            if not row:
                raise Exception("Unauthorized access or invalid watchlist.")

            conn.commit()

            return {
                "watchlist_id": row[0],
                "movie_id": row[1]
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")



def remove_movie_from_watchlist(watchlist_id: int, movie_id: int, user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                DELETE FROM watchlist_item
                WHERE watchlist_id = %s 
                  AND movie_id = %s
                  AND watchlist_id IN (
                      SELECT w.watchlist_id
                      FROM watchlist w
                      WHERE w.watchlist_id = %s AND w.user_id = %s
                  )
                RETURNING watchlist_id, movie_id;
            """
            cursor.execute(query, (watchlist_id, movie_id, watchlist_id, user_id))
            row = cursor.fetchone()

            if not row:
                raise Exception("Unauthorized access or invalid watchlist/movie combination.")
            
            conn.commit()

            return {
                "watchlist_id": row[0],
                "movie_id": row[1]
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")
        
def get_movies_from_watchlist(watchlist_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
            SELECT m.movie_id, m.title, m.release_year, d.name AS director_name
            FROM movie m
            JOIN director d ON m.director_id = d.director_id
            JOIN watchlist_item wi ON m.movie_id = wi.movie_id
            WHERE wi.watchlist_id = %s;
            """
            cursor.execute(query, (watchlist_id,))
            row = cursor.fetchall()

            if not row:
                raise Exception("Unauthorized access or invalid watchlist/movie combination.")
            
            conn.commit()

            return {
                "movie_id": row[0],
                "title": row[1],
                "release_year": row[2],
                "director_name": row[3]
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")

