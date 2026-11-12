# Architecture

[Back to README](README.md)

## Components

| Component | Source | Role |
| --- | --- | --- |
| FastAPI | backend/main.py | HTTP application, route registration, CORS, error handling |
| Configuration/security | backend/core/ | Environment settings and JWT/password helpers |
| PostgreSQL access | backend/database.py, backend/models/ | Async SQLAlchemy sessions and mapped entities |
| HTTP routes | backend/routes/ | Auth, pages, posts, intelligence |
| Input/output models | backend/schemas/ | Pydantic validation |
| Scoring | backend/intelligence/engine.py | Signals, weighted score, recommendations |
| Predictor | backend/ai_engine/virality_predictor.py | Feature extraction, training, saved models |
| Background tasks | backend/background_tasks/ | Mock sync, summaries, retraining schedule |
| React UI | frontend/src/ | Dashboard, login/register, pages, posts |
| Database migration | supabase/migrations/ | SQL schema and policy definitions |

## Request flow

Browser → Axios API client → FastAPI authentication/ownership checks → SQLAlchemy → PostgreSQL.

The client stores a token in localStorage and sends it as a Bearer token. Login uses form fields, not a JSON body. The database connection is direct; do not assume a custom JWT is automatically propagated as a Supabase authenticated identity.

An intelligence request reads the selected page's posts and daily metrics, computes signals, and stores an intelligence-score record. The GET intelligence endpoint therefore has a database-write side effect.

## Scoring

| Signal | Weight |
| --- | --- |
| Posting consistency | 0.10 |
| Reach trend | 0.15 |
| Conversion health | 0.15 |
| Momentum | 0.20 |
| Engagement stability | 0.10 |
| Viral probability | 0.20 |
| Content fatigue | -0.10 |

The weighted result is clamped to 0–100. Stages use thresholds 80, 60, and 40. The no-posts path reports Insufficient Data. Confidence is based on data completeness/quality heuristics, not calibration against future outcomes.

## Virality component

Features include post time/day/type, caption length, likes, comments, saves, and shares. The target is an engagement/reach heuristic. The predictor trains a StandardScaler and RandomForestRegressor when enough posts have positive reach and impressions (default minimum 10).

Model/scaler files are saved per page under AI_MODEL_PATH. On insufficient training data it falls back to recent-post heuristic scores. Existing engagement is part of the features, so this is not demonstrated pre-publication prediction. No held-out evaluation or measured accuracy is supplied.

## Background processing

The schedule uses UTC and defines daily mock sync plus weekly summaries/retraining. The mock sync changes follower counts and inserts randomized daily metrics. A weekly summary returns/logs results; no email delivery is implemented in that task.

Redis is configured for the Celery broker/results. The source does not establish Redis-backed user sessions or a finished response cache.

## Boundaries

Roles exist in user data, but a complete role-based permission matrix has not been verified. Neither table policies nor the presence of JWT helpers alone proves cross-user isolation. See [testing and limitations](docs/TESTING_AND_LIMITATIONS.md) before deployment.

Real Instagram OAuth/data ingestion, webhooks, and measured prediction quality remain unimplemented or unverified; they are not completed features.
