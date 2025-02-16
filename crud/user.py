from db import get_db



def fetch_followings(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT u.user_id, u.username, u.email
            FROM follow f
            JOIN "user" u ON f.following_id = u.user_id
            WHERE f.follower_id = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        # Listeyi dönüştürüp döndürelim
        return [{"user_id": row[0], "username": row[1], "email": row[2]} for row in result]
    

def fetch_followers(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT u.user_id, u.username, u.email
            FROM follow f
            JOIN "user" u ON f.follower_id = u.user_id
            WHERE f.following_id = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        # Listeyi dönüştürüp döndürelim
        return [{"user_id": row[0], "username": row[1], "email": row[2]} for row in result]


def create_follow_relationship(follower_id: int, following_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO follow (follower_id, following_id)
            VALUES (%s, %s)
            RETURNING follow_id;
        """
        cursor.execute(query, (follower_id, following_id))
        conn.commit()
        return cursor.fetchone()[0] 
    

def is_following(follower_id: int, following_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 1
            FROM follow
            WHERE follower_id = %s AND following_id = %s;
        """
        cursor.execute(query, (follower_id, following_id))
        result = cursor.fetchone()
        return result is not None
    

def delete_follow_relationship(follower_id: int, following_id: int) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            DELETE FROM follow
            WHERE follower_id = %s AND following_id = %s
            RETURNING follow_id;
        """
        cursor.execute(query, (follower_id, following_id))
        result = cursor.fetchone()
        conn.commit()

        # Eğer bir satır silinmişse, işlem başarılıdır
        return result is not None