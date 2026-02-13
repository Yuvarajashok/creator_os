from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from decimal import Decimal


class PostBase(BaseModel):
    instagram_post_id: str
    post_type: str
    caption: Optional[str] = None
    media_url: Optional[str] = None
    permalink: Optional[str] = None
    timestamp: datetime


class PostCreate(PostBase):
    page_id: UUID
    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    save_count: int = 0
    reach: int = 0
    impressions: int = 0
    engagement_rate: Decimal = Decimal("0")


class PostUpdate(BaseModel):
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    share_count: Optional[int] = None
    save_count: Optional[int] = None
    reach: Optional[int] = None
    impressions: Optional[int] = None
    engagement_rate: Optional[Decimal] = None


class PostResponse(PostBase):
    id: UUID
    page_id: UUID
    like_count: int
    comment_count: int
    share_count: int
    save_count: int
    reach: int
    impressions: int
    engagement_rate: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
