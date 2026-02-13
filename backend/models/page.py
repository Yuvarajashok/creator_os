from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instagram_username = Column(String, unique=True, nullable=False)
    instagram_id = Column(String, nullable=True)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    post_count = Column(Integer, default=0)
    bio = Column(String, nullable=True)
    profile_pic_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="pages")
    posts = relationship("Post", back_populates="page", cascade="all, delete-orphan")
    daily_metrics = relationship("DailyMetric", back_populates="page", cascade="all, delete-orphan")
    intelligence_scores = relationship("IntelligenceScore", back_populates="page", cascade="all, delete-orphan")
