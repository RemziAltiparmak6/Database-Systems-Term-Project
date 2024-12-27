from db import get_db

def insert_director(director):
    """
    Inserts a new director into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO director (name, biography, birth_date, place_of_birth)
            VALUES (%s, %s, %s, %s)
            RETURNING director_id;
        """
        cursor.execute(query, (director.name, director.biography, director.birth_date, director.place_of_birth))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added director


def fetch_director_by_id(director_id: int):
    """
    Fetches a director's details by their ID.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT director_id, name, biography, birth_date, place_of_birth
            FROM director
            WHERE director_id = %s;
        """
        cursor.execute(query, (director_id,))
        row = cursor.fetchone()
        return {
            "director_id": row[0],
            "name": row[1],
            "biography": row[2],
            "birth_date": row[3],
            "place_of_birth": row[4],
        } if row else None


def fetch_all_directors():
    """
    Fetches all directors from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT director_id, name, biography, birth_date, place_of_birth
            FROM director
            ORDER BY director_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [
            {
                "director_id": row[0],
                "name": row[1],
                "biography": row[2],
                "birth_date": row[3],
                "place_of_birth": row[4],
            }
            for row in result
        ]


def update_director(director_id: int, updated_data: dict):
    """
    Updates a director's details in the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        fields = [f"{key} = %s" for key in updated_data.keys()]
        values = list(updated_data.values())
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
