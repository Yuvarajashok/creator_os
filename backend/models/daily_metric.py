from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class DailyMetric(Base):
    __tablename__ = "daily_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    profile_visits = Column(Integer, default=0)
    website_clicks = Column(Integer, default=0)
    email_contacts = Column(Integer, default=0)
    engagement_total = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    page = relationship("Page", back_populates="daily_metrics")
