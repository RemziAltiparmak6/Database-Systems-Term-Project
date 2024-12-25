from db import get_db
from psycopg2.errors import IntegrityError
from psycopg2.extras import RealDictCursor




def check_user_exists_with_username(username: str, email: str):
    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM "user"
            WHERE username = %s OR email = %s;
        """
        cursor.execute(query, (username, email))
        count = cursor.fetchone()[0]
        return count > 0
    
def check_user_exists(username: str):
    with get_db() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)  # RealDictCursor kullanımı
        query = """
            SELECT * FROM "user"
            WHERE username = %s;
        """
        cursor.execute(query, (username,))
        user = cursor.fetchone()  # Kullanıcı bulunamazsa None döner
        return user

def insert_user(username: str, email: str, password: str):
    with get_db() as conn:
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO "user" (username, email, password, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING user_id;
            """
            cursor.execute(query, (username, email, password))
            conn.commit()
            return cursor.fetchone()[0]
        except IntegrityError as e:
            conn.rollback()  
            raise ValueError(f"Kullanıcı eklenirken hata oluştu: {str(e)}") 
        except Exception as e:
            conn.rollback()  
            raise ValueError(f"Beklenmeyen bir hata oluştu: {str(e)}")

