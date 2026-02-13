from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class IntelligenceScore(Base):
    __tablename__ = "intelligence_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"), nullable=False)
    overall_score = Column(Numeric, nullable=False)
    posting_consistency_score = Column(Numeric, default=0)
    reach_trend_score = Column(Numeric, default=0)
    conversion_health_score = Column(Numeric, default=0)
    momentum_score = Column(Numeric, default=0)
    engagement_stability_score = Column(Numeric, default=0)
    viral_probability_score = Column(Numeric, default=0)
    content_fatigue_penalty = Column(Numeric, default=0)
    growth_stage = Column(String, nullable=False)
    recommendations = Column(JSONB, default=[])
    confidence_score = Column(Numeric, default=0)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    page = relationship("Page", back_populates="intelligence_scores")
