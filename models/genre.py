from pydantic import BaseModel
from typing import Optional

# Create Model for Genre (for POST request)
class GenreCreate(BaseModel):
    name: str

# Response Model for Genre (for GET request)
class GenreResponse(BaseModel):
    genre_id: int
    name: str

# Update Model for Genre (for PUT request)
class GenreUpdate(BaseModel):
    name: Optional[str] = None
