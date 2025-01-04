from models.user import UserFollowingResponse,UserFollowerResponse, FollowResponse
from crud.user import fetch_followings, fetch_followers, create_follow_relationship, is_following, delete_follow_relationship
from fastapi import HTTPException



def get_followings_service(user_id: int) -> list[UserFollowingResponse]:
    try:
        followings = fetch_followings(user_id)

        if not followings:
            raise ValueError("No followings found for the given user.")

        return [UserFollowingResponse(**following) for following in followings]

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def get_followers_service(user_id: int) -> list[UserFollowerResponse]:
    try:
        followers = fetch_followers(user_id)

        if not followers:
            raise ValueError("No followers found for the given user.")

        return [UserFollowerResponse(**follower) for follower in followers]

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



def follow_user_service(follower_id: int, following_id: int) -> FollowResponse:
    try:
        if follower_id == following_id:
            raise ValueError("A user cannot follow themselves.")
        
        if is_following(follower_id, following_id):
            raise HTTPException(status_code=400, detail="User is already following this person.")

        follow_id = create_follow_relationship(follower_id, following_id)

        return FollowResponse(follow_id=follow_id, follower_id=follower_id, following_id=following_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    


def unfollow_user_service(follower_id: int, following_id: int) -> dict:
    try:
        if not is_following(follower_id, following_id):
            raise HTTPException(status_code=404, detail="You are not following this person.")

        success = delete_follow_relationship(follower_id, following_id)

        if not success:
            raise HTTPException(status_code=400, detail="Failed to unfollow the user.")

        return {"message": "Successfully unfollowed."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



    