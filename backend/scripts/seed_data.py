import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from database import AsyncSessionLocal
from models.user import User
from models.page import Page
from models.post import Post
from models.daily_metric import DailyMetric
from core.security import get_password_hash


async def seed_data():
    print("Starting data seeding...")

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).filter(User.email == "demo@creatoros.com"))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print("Demo user already exists. Skipping seed.")
            return

        demo_user = User(
            email="demo@creatoros.com",
            full_name="Demo User",
            hashed_password=get_password_hash("demo123456"),
            role="user",
            is_active=True
        )
        db.add(demo_user)
        await db.commit()
        await db.refresh(demo_user)
        print(f"✓ Created demo user: {demo_user.email}")

        demo_page = Page(
            user_id=demo_user.id,
            instagram_username="demo_creator",
            instagram_id="demo_123456",
            follower_count=15000,
            following_count=500,
            post_count=0,
            bio="Demo Instagram Creator Account - AI-Powered Growth",
            profile_pic_url=None,
            is_active=True
        )
        db.add(demo_page)
        await db.commit()
        await db.refresh(demo_page)
        print(f"✓ Created demo page: @{demo_page.instagram_username}")

        post_types = ['image', 'video', 'carousel', 'reel']
        posts = []

        for i in range(30):
            post_date = datetime.utcnow() - timedelta(days=29 - i)

            base_reach = random.randint(3000, 12000)
            base_engagement = int(base_reach * random.uniform(0.03, 0.08))

            like_count = int(base_engagement * random.uniform(0.7, 0.85))
            comment_count = int(base_engagement * random.uniform(0.05, 0.10))
            save_count = int(base_engagement * random.uniform(0.05, 0.08))
            share_count = int(base_engagement * random.uniform(0.02, 0.05))

            post = Post(
                page_id=demo_page.id,
                instagram_post_id=f"demo_post_{i+1}_{random.randint(1000, 9999)}",
                post_type=random.choice(post_types),
                caption=f"Demo post #{i+1} - This is sample content for testing the intelligence engine",
                media_url=None,
                permalink=f"https://instagram.com/p/demo_{i+1}",
                timestamp=post_date,
                like_count=like_count,
                comment_count=comment_count,
                share_count=share_count,
                save_count=save_count,
                reach=base_reach,
                impressions=int(base_reach * random.uniform(1.2, 1.5)),
                engagement_rate=(like_count + comment_count + save_count + share_count) / base_reach if base_reach > 0 else 0
            )
            posts.append(post)
            db.add(post)

        await db.commit()
        print(f"✓ Created {len(posts)} demo posts")

        demo_page.post_count = len(posts)
        await db.commit()

        metrics = []
        base_followers = 10000

        for i in range(30):
            metric_date = (datetime.utcnow() - timedelta(days=29 - i)).date()

            follower_growth = random.randint(100, 300)
            base_followers += follower_growth

            metric = DailyMetric(
                page_id=demo_page.id,
                date=metric_date,
                follower_count=base_followers,
                following_count=500,
                impressions=random.randint(8000, 20000),
                reach=random.randint(5000, 15000),
                profile_visits=random.randint(200, 800),
                website_clicks=random.randint(20, 100),
                email_contacts=random.randint(5, 30),
                engagement_total=random.randint(500, 2000)
            )
            metrics.append(metric)
            db.add(metric)

        await db.commit()
        print(f"✓ Created {len(metrics)} daily metrics")

        demo_page.follower_count = base_followers
        demo_page.last_synced_at = datetime.utcnow()
        await db.commit()

        print("\n" + "="*60)
        print("DATA SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nDemo Account Credentials:")
        print(f"  Email: demo@creatoros.com")
        print(f"  Password: demo123456")
        print(f"\nDemo Page:")
        print(f"  Username: @{demo_page.instagram_username}")
        print(f"  Followers: {demo_page.follower_count:,}")
        print(f"  Posts: {len(posts)}")
        print(f"  Daily Metrics: {len(metrics)}")
        print("\nYou can now:")
        print("  1. Login at http://localhost:3000/login")
        print("  2. View the dashboard")
        print("  3. Check intelligence scores")
        print("="*60)


if __name__ == "__main__":
    asyncio.run(seed_data())
