from models.user import UserResponse, UserCreate
from models.auth import LoginRequest, LoginResponse
from datetime import datetime
from crud.auth import insert_user, check_user_exists, check_user_exists_with_username
from passlib.hash import bcrypt
from helper import create_access_token



def sign_up_service(user_data: UserCreate) -> UserResponse:
    if check_user_exists_with_username(user_data.username, user_data.email):
        raise ValueError("Username or email already exists.")
    
    hashed_password = bcrypt.hash(user_data.password)

    # Kullanıcıyı veritabanına ekle
    user_id = insert_user(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )
    return UserResponse(
        user_id=user_id,    
        username=user_data.username,     #Buradaki verileri direkt girdiden alıyor.
        email=user_data.email,
        created_at=datetime.now()
    )


def login_user_service(username: str, password: str) -> LoginResponse:
    user = check_user_exists(username)
    if not user:
        raise ValueError("Kullanıcı bulunamadı.")
    
    # Şifre kontrolü
    if not bcrypt.verify(password, user["password"]):
        raise ValueError("Geçersiz şifre.")
    
    # Token oluştur
    token_data = {"user_id": user["user_id"], "username": user["username"]}
    access_token = create_access_token(data=token_data)
    
    return LoginResponse(access_token=access_token)



