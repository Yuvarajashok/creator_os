from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.page import Page
from models.post import Post
from models.daily_metric import DailyMetric
from ai_engine.virality_predictor import ViralityPredictor


class IntelligenceEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.weights = {
            'posting_consistency': 0.10,
            'reach_trend': 0.15,
            'conversion_health': 0.15,
            'momentum': 0.20,
            'engagement_stability': 0.10,
            'viral_probability': 0.20,
            'content_fatigue': -0.10
        }

    async def compute_intelligence_score(
        self,
        page_id: str,
        days: int = 30
    ) -> Dict[str, Any]:
        start_date = datetime.utcnow() - timedelta(days=days)

        page = await self._get_page(page_id)
        posts = await self._get_posts(page_id, start_date)
        metrics = await self._get_daily_metrics(page_id, start_date)

        if not posts:
            return self._generate_insufficient_data_response(page)

        signals = await self._compute_all_signals(page, posts, metrics, days)

        overall_score = self._calculate_weighted_score(signals)

        growth_stage = self._classify_growth_stage(overall_score)

        recommendations = self._generate_recommendations(signals, growth_stage)

        confidence_score = self._calculate_confidence(posts, metrics, days)

        return {
            'page_id': page_id,
            'instagram_username': page.instagram_username,
            'overall_score': round(overall_score, 2),
            'growth_stage': growth_stage,
            'confidence_score': round(confidence_score, 2),
            'signals': {k: round(v, 2) for k, v in signals.items()},
            'recommendations': recommendations,
            'key_metrics': self._extract_key_metrics(page, posts, metrics),
            'analysis_period_days': days,
            'generated_at': datetime.utcnow()
        }

    async def _get_page(self, page_id: str) -> Page:
        result = await self.db.execute(select(Page).filter(Page.id == page_id))
        return result.scalar_one()

    async def _get_posts(self, page_id: str, start_date: datetime) -> List[Post]:
        result = await self.db.execute(
            select(Post)
            .filter(Post.page_id == page_id, Post.timestamp >= start_date)
            .order_by(Post.timestamp.desc())
        )
        return result.scalars().all()

    async def _get_daily_metrics(self, page_id: str, start_date: datetime) -> List[DailyMetric]:
        result = await self.db.execute(
            select(DailyMetric)
            .filter(DailyMetric.page_id == page_id, DailyMetric.date >= start_date.date())
            .order_by(DailyMetric.date.asc())
        )
        return result.scalars().all()

    async def _compute_all_signals(
        self,
        page: Page,
        posts: List[Post],
        metrics: List[DailyMetric],
        days: int
    ) -> Dict[str, float]:
        return {
            'posting_consistency': self._compute_posting_consistency(posts, days),
            'reach_trend': self._compute_reach_trend(posts, metrics),
            'conversion_health': self._compute_conversion_health(metrics),
            'momentum': self._compute_momentum(metrics),
            'engagement_stability': self._compute_engagement_stability(posts),
            'viral_probability': await self._compute_viral_probability(page.id, posts),
            'content_fatigue': self._compute_content_fatigue(posts)
        }

    def _compute_posting_consistency(self, posts: List[Post], days: int) -> float:
        if not posts:
            return 0.0

        post_count = len(posts)
        expected_posts = days / 7 * 3
        consistency_ratio = min(post_count / expected_posts, 1.0)

        if post_count < 2:
            return consistency_ratio * 50

        timestamps = sorted([p.timestamp for p in posts])
        intervals = [(timestamps[i+1] - timestamps[i]).days for i in range(len(timestamps)-1)]

        if not intervals:
            return consistency_ratio * 50

        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)

        regularity_score = max(0, 1 - (std_interval / (mean_interval + 1)))

        score = (consistency_ratio * 0.6 + regularity_score * 0.4) * 100

        return min(score, 100.0)

    def _compute_reach_trend(self, posts: List[Post], metrics: List[DailyMetric]) -> float:
        if not posts or len(posts) < 2:
            return 50.0

        sorted_posts = sorted(posts, key=lambda x: x.timestamp)
        reaches = [p.reach for p in sorted_posts if p.reach > 0]

        if len(reaches) < 2:
            return 50.0

        mid_point = len(reaches) // 2
        first_half_avg = np.mean(reaches[:mid_point]) if mid_point > 0 else 0
        second_half_avg = np.mean(reaches[mid_point:])

        if first_half_avg == 0:
            growth_rate = 1.0
        else:
            growth_rate = (second_half_avg - first_half_avg) / first_half_avg

        score = 50 + (growth_rate * 100)
        return max(0, min(score, 100.0))

    def _compute_conversion_health(self, metrics: List[DailyMetric]) -> float:
        if not metrics:
            return 50.0

        total_reach = sum(m.reach for m in metrics)
        total_profile_visits = sum(m.profile_visits for m in metrics)

        if total_reach == 0:
            return 50.0

        conversion_rate = total_profile_visits / total_reach

        score = min(conversion_rate * 1000, 100)

        return score

    def _compute_momentum(self, metrics: List[DailyMetric]) -> float:
        if not metrics or len(metrics) < 2:
            return 50.0

        sorted_metrics = sorted(metrics, key=lambda x: x.date)

        follower_counts = [m.follower_count for m in sorted_metrics]

        if follower_counts[0] == 0:
            return 50.0

        total_growth = follower_counts[-1] - follower_counts[0]
        growth_rate = total_growth / follower_counts[0]

        days = len(metrics)
        daily_growth_rate = growth_rate / days if days > 0 else 0

        score = 50 + (daily_growth_rate * 5000)

        return max(0, min(score, 100.0))

    def _compute_engagement_stability(self, posts: List[Post]) -> float:
        if not posts or len(posts) < 2:
            return 50.0

        engagement_rates = [
            float(p.engagement_rate) for p in posts
            if p.engagement_rate is not None and p.reach > 0
        ]

        if len(engagement_rates) < 2:
            return 50.0

        mean_engagement = np.mean(engagement_rates)
        std_engagement = np.std(engagement_rates)

        if mean_engagement == 0:
            return 0.0

        coefficient_of_variation = std_engagement / mean_engagement

        stability_score = max(0, 1 - coefficient_of_variation)

        score = stability_score * 100

        return min(score, 100.0)

    async def _compute_viral_probability(self, page_id: str, posts: List[Post]) -> float:
        if not posts or len(posts) < 3:
            return 50.0

        try:
            predictor = ViralityPredictor()
            avg_probability = predictor.predict_virality(page_id, posts)
            return avg_probability * 100
        except Exception:
            engagement_rates = [float(p.engagement_rate) for p in posts if p.engagement_rate]
            if engagement_rates:
                avg_engagement = np.mean(engagement_rates)
                return min(avg_engagement * 1000, 100)
            return 50.0

    def _compute_content_fatigue(self, posts: List[Post]) -> float:
        if not posts or len(posts) < 3:
            return 0.0

        sorted_posts = sorted(posts, key=lambda x: x.timestamp)
        recent_posts = sorted_posts[-10:]

        if len(recent_posts) < 3:
            return 0.0

        engagement_rates = [float(p.engagement_rate) for p in recent_posts if p.engagement_rate]

        if len(engagement_rates) < 3:
            return 0.0

        trend = np.polyfit(range(len(engagement_rates)), engagement_rates, 1)[0]

        if trend < 0:
            fatigue_score = min(abs(trend) * 10000, 100)
        else:
            fatigue_score = 0.0

        return fatigue_score

    def _calculate_weighted_score(self, signals: Dict[str, float]) -> float:
        score = 0.0
        for signal_name, signal_value in signals.items():
            weight = self.weights.get(signal_name, 0)
            score += signal_value * weight

        return max(0, min(score, 100.0))

    def _classify_growth_stage(self, score: float) -> str:
        if score >= 80:
            return "Dominant Growth"
        elif score >= 60:
            return "Stable Growth"
        elif score >= 40:
            return "At Risk"
        else:
            return "Critical"

    def _generate_recommendations(self, signals: Dict[str, float], growth_stage: str) -> List[str]:
        recommendations = []

        if signals['posting_consistency'] < 60:
            recommendations.append("Increase posting frequency to 3-5 times per week for better consistency")

        if signals['reach_trend'] < 50:
            recommendations.append("Focus on creating shareable content to improve reach growth")

        if signals['conversion_health'] < 60:
            recommendations.append("Optimize your bio and call-to-actions to improve profile visit conversion")

        if signals['momentum'] < 50:
            recommendations.append("Engage more with your audience through comments and stories to boost follower growth")

        if signals['engagement_stability'] < 60:
            recommendations.append("Analyze your best-performing posts and replicate those content patterns")

        if signals['viral_probability'] < 60:
            recommendations.append("Experiment with trending formats and audio to increase viral potential")

        if signals['content_fatigue'] > 40:
            recommendations.append("Your audience may be experiencing content fatigue - try introducing new content pillars")

        if growth_stage == "Dominant Growth":
            recommendations.append("You're in dominant growth mode! Maintain your current strategy and consider content expansion")
        elif growth_stage == "Critical":
            recommendations.append("Urgent: Consider a content strategy reset and audience analysis")

        if not recommendations:
            recommendations.append("Keep up the great work! Continue monitoring your metrics for optimization opportunities")

        return recommendations[:6]

    def _calculate_confidence(self, posts: List[Post], metrics: List[DailyMetric], days: int) -> float:
        data_completeness = min(len(posts) / (days / 7 * 3), 1.0) * 0.5
        metrics_completeness = min(len(metrics) / days, 1.0) * 0.3

        data_quality = 0.2
        if posts:
            posts_with_metrics = sum(1 for p in posts if p.reach > 0 and p.impressions > 0)
            data_quality = (posts_with_metrics / len(posts)) * 0.2

        confidence = (data_completeness + metrics_completeness + data_quality) * 100

        return min(confidence, 100.0)

    def _extract_key_metrics(
        self,
        page: Page,
        posts: List[Post],
        metrics: List[DailyMetric]
    ) -> Dict[str, Any]:
        total_engagement = sum(
            p.like_count + p.comment_count + p.share_count + p.save_count
            for p in posts
        )

        avg_engagement_rate = (
            np.mean([float(p.engagement_rate) for p in posts if p.engagement_rate])
            if posts else 0
        )

        return {
            'current_followers': page.follower_count,
            'total_posts_analyzed': len(posts),
            'total_engagement': total_engagement,
            'avg_engagement_rate': round(avg_engagement_rate, 4),
            'avg_reach': round(np.mean([p.reach for p in posts if p.reach > 0]), 0) if posts else 0,
            'top_post_reach': max([p.reach for p in posts], default=0)
        }

    def _generate_insufficient_data_response(self, page: Page) -> Dict[str, Any]:
        return {
            'page_id': str(page.id),
            'instagram_username': page.instagram_username,
            'overall_score': 0,
            'growth_stage': 'Insufficient Data',
            'confidence_score': 0,
            'signals': {k: 0 for k in self.weights.keys()},
            'recommendations': [
                'Insufficient data for analysis',
                'Add posts and metrics to enable intelligence scoring',
                'Sync your Instagram data or add at least 10 posts'
            ],
            'key_metrics': {
                'current_followers': page.follower_count,
                'total_posts_analyzed': 0,
                'total_engagement': 0,
                'avg_engagement_rate': 0,
                'avg_reach': 0,
                'top_post_reach': 0
            },
            'analysis_period_days': 30,
            'generated_at': datetime.utcnow()
        }
