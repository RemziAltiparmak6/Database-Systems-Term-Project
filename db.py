#Postgre Database'e bağlanma ve işlemler için gerekli olan fonksiyonlar

import psycopg2
from contextlib import contextmanager
from fastapi import HTTPException
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
#DATABASE_URL = "postgresql://a1:T4njuk7zy12ct@34.69.231.245:5432/film_database?sslmode=require"

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



