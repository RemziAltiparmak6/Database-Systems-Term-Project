from models.user import UserFollowingResponse,UserFollowerResponse, FollowResponse
from crud.user import fetch_followings, fetch_followers, create_follow_relationship
from datetime import datetime


def get_followings_service(user_id: int) -> list[UserFollowingResponse]:
    followings = fetch_followings(user_id)  # CRUD'dan veriyi al
    # Gelen veriyi UserFollowingResponse formatına dönüştür
    return [UserFollowingResponse(**following) for following in followings]


def get_followers_service(user_id: int) -> list[UserFollowerResponse]:
    followers = fetch_followers(user_id)
    return [UserFollowingResponse(**follower) for follower in followers]


def follow_user_service(follower_id: int, following_id: int) -> FollowResponse:
    """
    Takip ilişkisini oluşturur ve bir response modeli döndürür.
    """
    if follower_id == following_id:
        raise ValueError("Kullanıcı kendini takip edemez.")  # İş mantığı kontrolü

    follow_id = create_follow_relationship(follower_id, following_id)  # CRUD katmanını çağır
    return FollowResponse(follow_id=follow_id, follower_id=follower_id, following_id=following_id)

    