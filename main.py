from fastapi import FastAPI
from db import get_connection  # Veritabanı bağlantı fonksiyonu
from routers.user import router as user_router  # User router
from routers.movie import router as movie_router  # Movie router

# FastAPI uygulamasını başlat
app = FastAPI()

# Router'ları uygulamaya dahil et
app.include_router(user_router)
app.include_router(movie_router)

# Başlangıç işlemleri
@app.on_event("startup")
async def startup():
    """
    Uygulama başlarken çalışacak işlemler.
    Örneğin, veritabanı bağlantısını başlatma.
    """
    try:
        connection = get_connection()  # Veritabanı bağlantısını test et
        if connection:
            print("Database connection established.")
    except Exception as e:
        print(f"Error establishing database connection: {e}")

# Kapanış işlemleri
@app.on_event("shutdown")
async def shutdown():
    """
    Uygulama kapanırken çalışacak işlemler.
    """
    print("Shutting down the application.")

# Kök endpoint
@app.get("/")
def read_root():
    """
    Basit bir karşılama endpoint'i.
    """
    return {"message": "Welcome to the Movie Platform API!"}
