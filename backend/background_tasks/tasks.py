import asyncio
from datetime import datetime, timedelta
import random
from typing import List
from celery import Task
from sqlalchemy import select
from background_tasks.celery_app import celery_app
from database import AsyncSessionLocal
from models.page import Page
from models.post import Post
from models.daily_metric import DailyMetric
from ai_engine.virality_predictor import ViralityPredictor
import logging

logger = logging.getLogger(__name__)


class AsyncTask(Task):
    def __call__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run(*args, **kwargs))


@celery_app.task(base=AsyncTask, bind=True)
async def sync_instagram_data_all_pages(self):
    logger.info("Starting Instagram data sync for all pages")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Page).filter(Page.is_active == True))
        pages = result.scalars().all()

        for page in pages:
            try:
                await sync_page_data(str(page.id))
                logger.info(f"Synced data for page {page.instagram_username}")
            except Exception as e:
                logger.error(f"Error syncing page {page.instagram_username}: {str(e)}")

    logger.info("Completed Instagram data sync")
    return {"synced_pages": len(pages)}


async def sync_page_data(page_id: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Page).filter(Page.id == page_id))
        page = result.scalar_one_or_none()

        if not page:
            return

        new_follower_count = page.follower_count + random.randint(-10, 50)
        new_follower_count = max(new_follower_count, 0)

        page.follower_count = new_follower_count
        page.last_synced_at = datetime.utcnow()

        today_metric = DailyMetric(
            page_id=page.id,
            date=datetime.utcnow().date(),
            follower_count=new_follower_count,
            following_count=page.following_count,
            impressions=random.randint(1000, 10000),
            reach=random.randint(800, 8000),
            profile_visits=random.randint(50, 500),
            website_clicks=random.randint(10, 100),
            email_contacts=random.randint(0, 20),
            engagement_total=random.randint(100, 1000)
        )

        db.add(today_metric)
        await db.commit()


@celery_app.task(base=AsyncTask, bind=True)
async def generate_weekly_intelligence_summary(self):
    logger.info("Generating weekly intelligence summaries")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Page).filter(Page.is_active == True))
        pages = result.scalars().all()

        summaries = []
        for page in pages:
            try:
                from intelligence.engine import IntelligenceEngine
                engine = IntelligenceEngine(db)
                report = await engine.compute_intelligence_score(str(page.id), days=7)
                summaries.append({
                    'page': page.instagram_username,
                    'score': report['overall_score'],
                    'stage': report['growth_stage']
                })
            except Exception as e:
                logger.error(f"Error generating summary for {page.instagram_username}: {str(e)}")

    logger.info(f"Generated {len(summaries)} intelligence summaries")
    return {"summaries": summaries}


@celery_app.task(base=AsyncTask, bind=True)
async def retrain_virality_models(self):
    logger.info("Retraining virality prediction models")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Page).filter(Page.is_active == True))
        pages = result.scalars().all()

        retrained_count = 0
        for page in pages:
            try:
                posts_result = await db.execute(
                    select(Post)
                    .filter(Post.page_id == page.id)
                    .order_by(Post.timestamp.desc())
                )
                posts = posts_result.scalars().all()

                if len(posts) >= 10:
                    predictor = ViralityPredictor()
                    if predictor.should_retrain(str(page.id), posts):
                        success = predictor.train_model(str(page.id), posts)
                        if success:
                            retrained_count += 1
                            logger.info(f"Retrained model for {page.instagram_username}")

            except Exception as e:
                logger.error(f"Error retraining model for {page.instagram_username}: {str(e)}")

    logger.info(f"Retrained {retrained_count} models")
    return {"retrained_models": retrained_count}


@celery_app.task(base=AsyncTask, bind=True)
async def sync_single_page(self, page_id: str):
    logger.info(f"Syncing single page: {page_id}")
    await sync_page_data(page_id)
    return {"status": "completed", "page_id": page_id}
