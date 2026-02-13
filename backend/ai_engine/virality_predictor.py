import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import List, Optional
from datetime import datetime
from models.post import Post
from core.config import settings


class ViralityPredictor:
    def __init__(self):
        self.model_dir = settings.AI_MODEL_PATH
        self.min_posts_for_training = settings.MIN_POSTS_FOR_TRAINING
        self.model: Optional[RandomForestRegressor] = None
        self.scaler: Optional[StandardScaler] = None
        self._ensure_model_dir()

    def _ensure_model_dir(self):
        os.makedirs(self.model_dir, exist_ok=True)

    def _get_model_path(self, page_id: str) -> str:
        return os.path.join(self.model_dir, f"virality_model_{page_id}.pkl")

    def _get_scaler_path(self, page_id: str) -> str:
        return os.path.join(self.model_dir, f"scaler_{page_id}.pkl")

    def _load_model(self, page_id: str) -> bool:
        model_path = self._get_model_path(page_id)
        scaler_path = self._get_scaler_path(page_id)

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
                return True
            except Exception:
                return False
        return False

    def _save_model(self, page_id: str):
        if self.model and self.scaler:
            model_path = self._get_model_path(page_id)
            scaler_path = self._get_scaler_path(page_id)
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)

    def _extract_features(self, post: Post) -> np.ndarray:
        hour_of_day = post.timestamp.hour
        day_of_week = post.timestamp.weekday()

        post_type_encoding = {
            'image': 0,
            'video': 1,
            'carousel': 2,
            'reel': 3
        }
        post_type_encoded = post_type_encoding.get(post.post_type, 0)

        caption_length = len(post.caption) if post.caption else 0

        features = [
            hour_of_day,
            day_of_week,
            post_type_encoded,
            caption_length,
            post.like_count,
            post.comment_count,
            post.save_count,
            post.share_count,
        ]

        return np.array(features).reshape(1, -1)

    def _calculate_virality_score(self, post: Post) -> float:
        if post.reach == 0:
            return 0.0

        engagement = post.like_count + post.comment_count + (post.save_count * 2) + (post.share_count * 3)
        virality = engagement / post.reach

        return min(virality, 1.0)

    def train_model(self, page_id: str, posts: List[Post]) -> bool:
        if len(posts) < self.min_posts_for_training:
            return False

        posts_with_metrics = [
            p for p in posts
            if p.reach > 0 and p.impressions > 0
        ]

        if len(posts_with_metrics) < self.min_posts_for_training:
            return False

        X = []
        y = []

        for post in posts_with_metrics:
            features = self._extract_features(post)
            virality_score = self._calculate_virality_score(post)

            X.append(features.flatten())
            y.append(virality_score)

        X = np.array(X)
        y = np.array(y)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        self.model.fit(X_scaled, y)

        self._save_model(page_id)

        return True

    def predict_virality(self, page_id: str, posts: List[Post]) -> float:
        if not self._load_model(page_id):
            success = self.train_model(page_id, posts)
            if not success:
                recent_posts = sorted(posts, key=lambda x: x.timestamp, reverse=True)[:5]
                if recent_posts:
                    virality_scores = [self._calculate_virality_score(p) for p in recent_posts]
                    return np.mean(virality_scores)
                return 0.5

        recent_posts = sorted(posts, key=lambda x: x.timestamp, reverse=True)[:5]

        if not recent_posts:
            return 0.5

        predictions = []
        for post in recent_posts:
            features = self._extract_features(post)
            features_scaled = self.scaler.transform(features)
            prediction = self.model.predict(features_scaled)[0]
            predictions.append(max(0, min(prediction, 1)))

        return np.mean(predictions)

    def should_retrain(self, page_id: str, posts: List[Post]) -> bool:
        model_path = self._get_model_path(page_id)

        if not os.path.exists(model_path):
            return True

        model_age_days = (datetime.now() - datetime.fromtimestamp(os.path.getmtime(model_path))).days

        if model_age_days > 30:
            return True

        posts_with_metrics = [p for p in posts if p.reach > 0]
        if len(posts_with_metrics) >= self.min_posts_for_training * 2:
            return True

        return False
