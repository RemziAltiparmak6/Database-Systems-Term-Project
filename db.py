#Postgre Database'e bağlanma ve işlemler için gerekli olan fonksiyonlar

import psycopg2
from contextlib import contextmanager
from fastapi import HTTPException
from dotenv import load_dotenv
import os


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

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



