from db import get_db

def add_award(award):
    """
    Inserts a new award into the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO award (name, year)
            VALUES (%s, %s)
            RETURNING award_id;
        """
        cursor.execute(query, (award.name, award.year))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the newly added award

def update_award(award_id: int, updated_data: dict):
    """
    Updates an award's details in the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        fields = []
        values = []
        for key, value in updated_data.items():
            fields.append(f"{key} = %s")
            values.append(value)
        values.append(award_id)
        query = f"""
            UPDATE award
            SET {', '.join(fields)}
            WHERE award_id = %s
            RETURNING award_id;
        """
        cursor.execute(query, tuple(values))
        conn.commit()
        return cursor.fetchone()[0]  # Return the ID of the updated award

def delete_award(award_id: int):
    """
    Deletes an award from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = "DELETE FROM award WHERE award_id = %s;"
        cursor.execute(query, (award_id,))
        conn.commit()

def get_all_awards():
    """
    Fetches all awards from the database.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT award_id, name, year
            FROM award
            ORDER BY award_id ASC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return [{"award_id": row[0], "name": row[1], "year": row[2]} for row in result]
