from pydantic import BaseModel, Field
from typing import List, Optional, Literal

Gender = Literal["male", "female"]
Status = Literal["draft", "pending", "active", "blocked"]


class ProfileCreateIn(BaseModel):
    gender: Gender
    display_name: str = Field(min_length=1, max_length=128)
    age: int = Field(ge=18, le=99)
    region: str = Field(min_length=2)
    city: str = ""
    tg_username_public: str
    bio: str = ""
    photos: list[str] = []

class ProfileOut(BaseModel):
    id: str
    owner_user_id: str
    gender: Gender
    display_name: str
    bio: str
    age: int
    city: str
    tg_username_public: str
    photos: List[str]
    status: Status
    active_until: Optional[str] = None
    vip_until: Optional[str] = None


class ContactOut(BaseModel):
    locked: bool
    username: Optional[str] = None