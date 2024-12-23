#Postgre Database'e bağlanma ve işlemler için gerekli olan fonksiyonlar

import psycopg2
from contextlib import contextmanager
from fastapi import HTTPException


DATABASE_URL = "postgresql://a1:123456@34.77.191.120:5432/movie_platform"

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        raise HTTPException(status_code = 500,  detail=f"Database connection error: {str(e)}")


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()



