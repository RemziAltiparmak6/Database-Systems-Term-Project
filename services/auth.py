from models.user import UserResponse, UserCreate
from models.auth import LoginRequest, LoginResponse
from datetime import datetime
from crud.auth import insert_user, check_user_exists, check_user_exists_with_username
from passlib.hash import bcrypt
from helper import create_access_token
from fastapi import HTTPException



def sign_up_service(user_data: UserCreate) -> UserResponse:
    if check_user_exists_with_username(user_data.username, user_data.email):
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    hashed_password = bcrypt.hash(user_data.password)

    # Kullanıcıyı veritabanına ekle
    user_id = insert_user(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role
    )
    return UserResponse(
        user_id=user_id,    
        username=user_data.username, 
        email=user_data.email,
        created_at=datetime.now()
    )

# Login service
def login_user_service(username: str, password: str) -> LoginResponse:
    user = check_user_exists(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Şifre kontrolü
    if not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password.")

    # Token oluştur
    token_data = {"user_id": user["user_id"], "username": user["username"], "role": user["role"]}               
    access_token = create_access_token(data=token_data)

    return LoginResponse(access_token=access_token)



