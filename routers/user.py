from fastapi import APIRouter
from models.user import UserCreate, UserResponse, UserFollowingResponse, UserFollowerResponse, FollowResponse
from services.user import create_user_service, get_followings_service, get_followers_service, follow_user_service


router = APIRouter(
    prefix="/users",  # Tüm endpoint'ler /users ile başlayacak
    tags=["Users"]    # Swagger dokümantasyonu için grup etiketi
)

@router.post("/", response_model = UserResponse)
def create_user(User: UserCreate):
    return create_user_service(User)

@router.get("/{user_id}/followings", response_model=list[UserFollowingResponse])          #Buna bir response model lazım
def get_followings(user_id: int):
    return get_followings_service(user_id)


@router.get("/{user_id}/followers", response_model=list[UserFollowerResponse])          #Buna bir response model lazım
def get_followers(user_id: int):
    return get_followers_service(user_id)


@router.post("/{user_id}/follow", response_model=FollowResponse)
def follow(user_id: int, follow_id: int):
    return follow_user_service(user_id, follow_id)