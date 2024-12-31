from pydantic import BaseModel
from typing import Optional

# Create Model for Award (for POST request)
class AwardCreate(BaseModel):
    name: str
    year: int

# Response Model for Award (for GET request)
class AwardResponse(BaseModel):
    award_id: int
    name: str
    year: int

# Update Model for Award (for PUT request)
class AwardUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
