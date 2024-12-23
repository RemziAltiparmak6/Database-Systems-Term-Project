from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserFollowingResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class UserFollowerResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr


class FollowResponse(BaseModel):
    follow_id: int
    follower_id: int
    following_id: int

