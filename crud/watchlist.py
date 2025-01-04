from db import get_db



def get_watchlist_owner(watchlist_id: int) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT user_id FROM watchlist WHERE watchlist_id = %s;"
        cursor.execute(query, (watchlist_id,))
        owner = cursor.fetchone()
        if not owner:
            raise ValueError("Watchlist not found")
        return owner[0]  # Watchlist'in sahibinin user_id'sini döner


    
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
        

def update_watchlist(watchlist_id: int, name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                UPDATE watchlist
                SET name = %s
                WHERE watchlist_id = %s
                RETURNING watchlist_id, user_id, name, created_at;
            """
            cursor.execute(query, (name, watchlist_id))
            row = cursor.fetchone()
            conn.commit()

            if not row:
                raise Exception("Watchlist not found")

            return {
                "watchlist_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "created_at": row[3],
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")
        

def delete_watchlist(watchlist_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                DELETE FROM watchlist
                WHERE watchlist_id = %s 
                RETURNING watchlist_id, user_id, name, created_at;
            """
            cursor.execute(query, (watchlist_id,))
            row = cursor.fetchone()
            conn.commit()

            if not row:
                raise Exception("Watchlist not found")

            return {
                "watchlist_id": row[0],
                "user_id": row[1],
                "name": row[2],
                "created_at": row[3],
            }
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")
        

def fetch_movies_in_watchlist(watchlist_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    m.movie_id, 
                    m.title, 
                    m.release_year, 
                    d.name AS director_name
                FROM 
                    movie m
                JOIN 
                    director d 
                ON 
                    m.director_id = d.director_id
                JOIN 
                    watchlist_item wm 
                ON 
                    m.movie_id = wm.movie_id
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
        
def fetch_watchlists(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            query = """
                SELECT 
                    watchlist_id, 
                    name, 
                    created_at
                FROM 
                    watchlist
                WHERE 
                    user_id = %s;
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            return [
                {
                    "watchlist_id": row[0],
                    "user_id": user_id,
                    "name": row[1],
                    "created_at": row[2]
                }
                for row in rows
            ]
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
        
        

        
def add_movie_to_watchlist(watchlist_id: int, movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # İzleme listesine film ekle
            query = """
                INSERT INTO watchlist_item (watchlist_id, movie_id)
                SELECT w.watchlist_id, %s
                FROM watchlist w
                WHERE w.watchlist_id = %s
                RETURNING watchlist_id, movie_id;
            """
            cursor.execute(query, (movie_id, watchlist_id))
            row = cursor.fetchone()
            conn.commit()

            if not row:
                raise Exception("Failed to add movie to watchlist")

            # Film detaylarını al
            movie_query = """
                SELECT m.movie_id, m.title, m.release_year, d.name AS director_name
                FROM movie m
                JOIN director d ON m.director_id = d.director_id
                WHERE m.movie_id = %s;
            """
            cursor.execute(movie_query, (movie_id,))
            movie_row = cursor.fetchone()

            if not movie_row:
                raise Exception("Movie not found")

            # movie_row'u sözlüğe dönüştür
            movie_data = {
                "movie_id": movie_row[0],
                "title": movie_row[1],
                "release_year": movie_row[2],
                "director_name": movie_row[3]
            }

            return movie_data
        except Exception as e:
            conn.rollback()
            raise Exception(f"Database error: {str(e)}")





def remove_movie_from_watchlist(watchlist_id: int, movie_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            # İzleme listesinden filmi sil
            query = """
                DELETE FROM watchlist_item
                WHERE watchlist_id = %s 
                  AND movie_id = %s
                  AND watchlist_id IN (
                      SELECT w.watchlist_id
                      FROM watchlist w
                      WHERE w.watchlist_id = %s
                  )
                RETURNING watchlist_id, movie_id;
            """
            cursor.execute(query, (watchlist_id, movie_id, watchlist_id))
            row = cursor.fetchone()

            if not row:
                raise Exception("Unauthorized access or invalid watchlist/movie combination.")

            # Film detaylarını almak için sorgu
            movie_query = """
                SELECT m.movie_id, m.title, m.release_year, d.name AS director_name
                FROM movies m
                JOIN directors d ON m.director_id = d.director_id
                WHERE m.movie_id = %s;
            """
            cursor.execute(movie_query, (movie_id,))
            movie_row = cursor.fetchone()

            if not movie_row:
                raise Exception("Movie not found.")

            conn.commit()
            return {
                "movie_id": movie_row[0],
                "title": movie_row[1],
                "release_year": movie_row[2],
                "director_name": movie_row[3]
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
        




