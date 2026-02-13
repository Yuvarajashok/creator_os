from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class PageBase(BaseModel):
    instagram_username: str
    bio: Optional[str] = None


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    instagram_username: Optional[str] = None
    bio: Optional[str] = None
    instagram_id: Optional[str] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    post_count: Optional[int] = None
    profile_pic_url: Optional[str] = None
    is_active: Optional[bool] = None


class PageResponse(PageBase):
    id: UUID
    user_id: UUID
    instagram_id: Optional[str]
    follower_count: int
    following_count: int
    post_count: int
    profile_pic_url: Optional[str]
    is_active: bool
    last_synced_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
