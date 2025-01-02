from db import get_db

def insert_actor(actor):
    """
    Inserts a new actor into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO actor (name, nationality, birth_year)
            VALUES (%s, %s, %s)
            RETURNING actor_id;
        """
        cursor.execute(query, (actor.name, actor.nationality, actor.birth_year))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added actor
    
    
def delete_actor(actor_id: int):
    """
    Deletes an actor from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = "DELETE FROM actor WHERE actor_id = %s;"
        cursor.execute(query, (actor_id,))
        conn.commit()

def fetch_actor_by_id(actor_id: int):
    """
    Fetches an actor's details by their ID.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT actor_id, name, nationality, birth_year
            FROM actor
            WHERE actor_id = %s;
        """
        cursor.execute(query, (actor_id,))
        row = cursor.fetchone()
        if row:
            return {
                "actor_id": row[0],
                "name": row[1],
                "nationality": row[2],
                "birth_year": row[3],
            }
        return None  # Return None if no actor found

def fetch_all_actors():
    """
    Fetches all actors from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT actor_id, name, nationality, birth_year
            FROM actor
            ORDER BY actor_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [
            {
                "actor_id": row[0],
                "name": row[1],
                "nationality": row[2],
                "birth_year": row[3],
            } for row in result
        ]

def update_actor(actor_id: int, updated_data: dict):
    """
    Updates an actor's details in the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in updated_data.items():
            if key != 'biography':  # Exclude the biography field (if any)
                fields.append(f"{key} = %s")
                values.append(value)
        values.append(actor_id)
        query = f"""
            UPDATE actor
            SET {', '.join(fields)}
            WHERE actor_id = %s
            RETURNING actor_id;
        """
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the updated actor

# Get all movies for a specific actor
def get_movies_for_actor(actor_id: int):
    query = """
    SELECT m.movie_id, m.title, m.director_id, m.release_year
    FROM movie m
    JOIN movie_actor ma ON m.movie_id = ma.movie_id
    WHERE ma.actor_id = %s;
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (actor_id,))
        return cursor.fetchall()
