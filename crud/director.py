from db import get_db



def insert_director(director):
    """
    Inserts a new director into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO director (name, nationality, birth_year)
            VALUES (%s, %s, %s)
            RETURNING director_id;
        """
        cursor.execute(query, (director.name, director.nationality, director.birth_year))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added director


def fetch_director_by_id(director_id: int):
    """
    Fetches a director's details by their ID.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT director_id, name, nationality, birth_year
            FROM director
            WHERE director_id = %s;
        """
        cursor.execute(query, (director_id,))
        row = cursor.fetchone()
        if row:
            return {
                "director_id": row[0],
                "name": row[1],
                "nationality": row[2],
                "birth_year": row[3],
            }
        return None  # Return None if no director found
    
    
    
    
def fetch_all_directors():
    """
    Fetches all directors from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT director_id, name, nationality, birth_year
            FROM director
            ORDER BY director_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [
            {
                "director_id": row[0],
                "name": row[1],
                "nationality": row[2],
                "birth_year": row[3],
            } for row in result
        ]


def update_director(director_id: int, updated_data: dict):
    """
    Updates a director's details in the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in updated_data.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(director_id)
        query = f"""
            UPDATE director
            SET {', '.join(fields)}
            WHERE director_id = %s
            RETURNING director_id;
        """
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the updated director
    
    
def get_movies_for_director(director_id: int):
    """
    Retrieves all movies for a specific director.
    """
    query = """
    SELECT m.movie_id, m.title, m.director_id, m.release_year
    FROM movie m
    WHERE m.director_id = %s;
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (director_id,))
        return cursor.fetchall()