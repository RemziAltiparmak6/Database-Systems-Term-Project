from db import get_db

def insert_actor(actor):
    """
    Inserts a new actor into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO actor (name, biography, birth_date, place_of_birth)
            VALUES (%s, %s, %s, %s)
            RETURNING actor_id;
        """
        cursor.execute(query, (actor.name, actor.biography, actor.birth_date, actor.place_of_birth))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added actor

def fetch_actor_by_id(actor_id: int):
    """
    Fetches an actor's details by their ID.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT actor_id, name, biography, birth_date, place_of_birth
            FROM actor
            WHERE actor_id = %s;
        """
        cursor.execute(query, (actor_id,))
        row = cursor.fetchone()
        if row:
            return {
                "actor_id": row[0],
                "name": row[1],
                "biography": row[2],
                "birth_date": row[3],
                "place_of_birth": row[4]
            }
        return None  # Return None if no actor found

def fetch_all_actors():
    """
    Fetches all actors from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT actor_id, name, biography, birth_date, place_of_birth
            FROM actor
            ORDER BY actor_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [
            {
                "actor_id": row[0],
                "name": row[1],
                "biography": row[2],
                "birth_date": row[3],
                "place_of_birth": row[4]
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
    SELECT m.title, m.release_date, m.vote_average
    FROM movie m
    JOIN movie_actor ma ON m.movie_id = ma.movie_id
    WHERE ma.actor_id = %s;
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (actor_id,))
        return cursor.fetchall()

# Get the highest-rated movie for a specific actor
def get_top_movie_for_actor(actor_id: int):
    query = """
    SELECT m.title, m.vote_average
    FROM movie m
    JOIN movie_actor ma ON m.movie_id = ma.movie_id
    WHERE ma.actor_id = %s
    ORDER BY m.vote_average DESC
    LIMIT 1;
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (actor_id,))
        return cursor.fetchone()