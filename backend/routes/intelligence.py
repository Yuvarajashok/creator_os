from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any
from uuid import UUID

from database import get_db
from models.user import User
from models.page import Page
from models.intelligence_score import IntelligenceScore
from schemas.intelligence import IntelligenceReport
from core.security import get_current_user
from intelligence.engine import IntelligenceEngine

router = APIRouter()


async def verify_page_ownership(page_id: UUID, user_id: UUID, db: AsyncSession) -> Page:
    result = await db.execute(
        select(Page).filter(Page.id == page_id, Page.user_id == user_id)
    )
    page = result.scalar_one_or_none()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Page not found or access denied"
        )

    return page


@router.get("/{page_id}", response_model=IntelligenceReport)
async def get_intelligence_score(
    page_id: UUID,
    days: int = Query(default=30, ge=7, le=90),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    await verify_page_ownership(page_id, current_user.id, db)

    engine = IntelligenceEngine(db)

    report = await engine.compute_intelligence_score(str(page_id), days)

    intelligence_score = IntelligenceScore(
        page_id=page_id,
        overall_score=report['overall_score'],
        posting_consistency_score=report['signals']['posting_consistency'],
        reach_trend_score=report['signals']['reach_trend'],
        conversion_health_score=report['signals']['conversion_health'],
        momentum_score=report['signals']['momentum'],
        engagement_stability_score=report['signals']['engagement_stability'],
        viral_probability_score=report['signals']['viral_probability'],
        content_fatigue_penalty=report['signals']['content_fatigue'],
        growth_stage=report['growth_stage'],
        recommendations=report['recommendations'],
        confidence_score=report['confidence_score'],
        metadata=report['key_metrics']
    )

    db.add(intelligence_score)
    await db.commit()

    return report
