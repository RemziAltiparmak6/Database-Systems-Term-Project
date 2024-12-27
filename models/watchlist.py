from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class WatchlistCreate(BaseModel):
    name: str = Field(..., max_length=50)  # Maksimum uzunluk 50 karakter

class WatchlistResponse(BaseModel):
    watchlist_id: int
    user_id: int
    name: str
    created_at: datetime

