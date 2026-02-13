from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
from uuid import UUID
from decimal import Decimal


class IntelligenceScoreResponse(BaseModel):
    id: UUID
    page_id: UUID
    overall_score: Decimal
    posting_consistency_score: Decimal
    reach_trend_score: Decimal
    conversion_health_score: Decimal
    momentum_score: Decimal
    engagement_stability_score: Decimal
    viral_probability_score: Decimal
    content_fatigue_penalty: Decimal
    growth_stage: str
    recommendations: List[str]
    confidence_score: Decimal
    metadata: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class IntelligenceReport(BaseModel):
    page_id: UUID
    instagram_username: str
    overall_score: float
    growth_stage: str
    confidence_score: float
    signals: Dict[str, float]
    recommendations: List[str]
    key_metrics: Dict[str, Any]
    analysis_period_days: int
    generated_at: datetime
