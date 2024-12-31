from fastapi import APIRouter,Depends
from models.user import UserCreate, UserResponse, UserFollowingResponse, UserFollowerResponse, FollowResponse
from services.user import get_followings_service, get_followers_service, follow_user_service
from helper import get_current_user


router = APIRouter(
    prefix="/users",  # Tüm endpoint'ler /users ile başlayacak
    tags=["Users"]    # Swagger dokümantasyonu için grup etiketi
)


@router.get("/{user_id}/followings", response_model=list[UserFollowingResponse])          #Buna bir response model lazım
def get_followings(user_id: int, current_user: dict = Depends(get_current_user)):
    return get_followings_service(user_id)


@router.get("/{user_id}/followers", response_model=list[UserFollowerResponse])          #Buna bir response model lazım
def get_followers(user_id: int, current_user: dict = Depends(get_current_user)):
    return get_followers_service(user_id)


@router.post("/follow", response_model=FollowResponse)
def follow(follow_id: int, current_user: dict = Depends(get_current_user)):
    return follow_user_service(current_user["user_id"], follow_id)