from db import get_db

def add_genre(genre):
    """
    Inserts a new genre into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO genre (name)
            VALUES (%s)
            RETURNING genre_id;
        """
        cursor.execute(query, (genre.name,))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added genre

def update_genre(genre_id: int, updated_data: dict):
    """
    Updates a genre's details in the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in updated_data.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(genre_id)
        query = f"""
            UPDATE genre
            SET {', '.join(fields)}
            WHERE genre_id = %s
            RETURNING genre_id;
        """
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the updated genre

def delete_genre(genre_id: int):
    """
    Deletes a genre from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = "DELETE FROM genre WHERE genre_id = %s;"
        cursor.execute(query, (genre_id,))
        conn.commit()

def get_all_genres():
    """
    Fetches all genres from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT genre_id, name
            FROM genre
            ORDER BY genre_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [{"genre_id": row[0], "name": row[1]} for row in result]
