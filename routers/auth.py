from fastapi import APIRouter
from models.user import UserResponse, UserCreate
from models.auth import LoginRequest, LoginResponse
from services.auth import sign_up_service, login_user_service
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm




router = APIRouter(
    prefix="/auth",  # Tüm endpoint'ler /users ile başlayacak
    tags=["Auth"]    # Swagger dokümantasyonu için grup etiketi
)

@router.post("/signup/", response_model = UserResponse)
def sign_up(User: UserCreate):
    return sign_up_service(User)


@router.post("/login", response_model=LoginResponse)
def login_json(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username, form_data.password)
    try:
        return login_user_service(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



