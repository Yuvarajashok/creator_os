# Creator OS API Documentation

Base URL: `http://localhost:8000` (development)

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <token>
```

### Register

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response** (201):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Login

```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response** (200):
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Pages

### List Pages

```http
GET /api/v1/pages/
Authorization: Bearer <token>
```

**Response** (200):
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "instagram_username": "demo_creator",
    "instagram_id": "123456",
    "follower_count": 15000,
    "following_count": 500,
    "post_count": 30,
    "bio": "Creator bio",
    "profile_pic_url": null,
    "is_active": true,
    "last_synced_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get Page

```http
GET /api/v1/pages/{page_id}
Authorization: Bearer <token>
```

### Create Page

```http
POST /api/v1/pages/
Authorization: Bearer <token>
Content-Type: application/json

{
  "instagram_username": "new_creator",
  "bio": "Optional bio"
}
```

**Response** (201): Page object

### Update Page

```http
PUT /api/v1/pages/{page_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "bio": "Updated bio",
  "follower_count": 15500
}
```

### Delete Page

```http
DELETE /api/v1/pages/{page_id}
Authorization: Bearer <token>
```

**Response** (204): No content

## Posts

### Get Page Posts

```http
GET /api/v1/posts/page/{page_id}
Authorization: Bearer <token>
```

**Response** (200):
```json
[
  {
    "id": "uuid",
    "page_id": "uuid",
    "instagram_post_id": "post_123",
    "post_type": "image",
    "caption": "Post caption",
    "media_url": "https://...",
    "permalink": "https://instagram.com/p/...",
    "timestamp": "2024-01-01T00:00:00Z",
    "like_count": 1500,
    "comment_count": 50,
    "share_count": 20,
    "save_count": 80,
    "reach": 10000,
    "impressions": 12000,
    "engagement_rate": 0.165,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### Create Post

```http
POST /api/v1/posts/
Authorization: Bearer <token>
Content-Type: application/json

{
  "page_id": "uuid",
  "instagram_post_id": "unique_post_id",
  "post_type": "image",
  "caption": "Post caption",
  "timestamp": "2024-01-01T12:00:00Z",
  "like_count": 100,
  "comment_count": 5,
  "share_count": 2,
  "save_count": 8,
  "reach": 1000,
  "impressions": 1200,
  "engagement_rate": 0.115
}
```

### Update Post

```http
PUT /api/v1/posts/{post_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "like_count": 150,
  "comment_count": 10
}
```

### Delete Post

```http
DELETE /api/v1/posts/{post_id}
Authorization: Bearer <token>
```

## Intelligence

### Get Intelligence Score

```http
GET /api/v1/intelligence/{page_id}?days=30
Authorization: Bearer <token>
```

**Query Parameters**:
- `days` (optional): Number of days to analyze (7-90, default: 30)

**Response** (200):
```json
{
  "page_id": "uuid",
  "instagram_username": "demo_creator",
  "overall_score": 72.5,
  "growth_stage": "Stable Growth",
  "confidence_score": 85.2,
  "signals": {
    "posting_consistency": 75.0,
    "reach_trend": 68.5,
    "conversion_health": 72.3,
    "momentum": 80.1,
    "engagement_stability": 71.8,
    "viral_probability": 65.4,
    "content_fatigue": 15.2
  },
  "recommendations": [
    "Increase posting frequency to 3-5 times per week",
    "Focus on creating shareable content",
    "Optimize your bio for better conversions"
  ],
  "key_metrics": {
    "current_followers": 15000,
    "total_posts_analyzed": 30,
    "total_engagement": 5000,
    "avg_engagement_rate": 0.055,
    "avg_reach": 8500,
    "top_post_reach": 15000
  },
  "analysis_period_days": 30,
  "generated_at": "2024-01-01T00:00:00Z"
}
```

## Intelligence Scoring System

### Overall Score Calculation

```
Overall Score =
  (Posting Consistency × 0.10) +
  (Reach Trend × 0.15) +
  (Conversion Health × 0.15) +
  (Momentum × 0.20) +
  (Engagement Stability × 0.10) +
  (Viral Probability × 0.20) -
  (Content Fatigue × 0.10)
```

### Growth Stages

| Score Range | Stage | Description |
|-------------|-------|-------------|
| 80-100 | Dominant Growth | Exceptional performance across all metrics |
| 60-79 | Stable Growth | Good performance with room for optimization |
| 40-59 | At Risk | Multiple areas need attention |
| 0-39 | Critical | Urgent action required |

### Signal Definitions

**Posting Consistency** (0-100):
- Measures posting frequency and regularity
- Higher score = more consistent posting schedule

**Reach Trend** (0-100):
- Analyzes reach growth over time
- Higher score = increasing reach

**Conversion Health** (0-100):
- Profile visits / reach ratio
- Higher score = better conversion rate

**Momentum** (0-100):
- Follower growth rate
- Higher score = faster growth

**Engagement Stability** (0-100):
- Consistency of engagement rates
- Higher score = more stable engagement

**Viral Probability** (0-100):
- ML-predicted likelihood of viral content
- Based on historical performance

**Content Fatigue** (0-100):
- Declining engagement trend detection
- Higher score = more fatigue (negative signal)

## Health Check

```http
GET /health
```

**Response** (200):
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently no rate limiting implemented. For production, consider:
- 100 requests per minute per user
- 1000 requests per hour per IP

## Webhooks

Not currently implemented. Future feature for:
- Intelligence score updates
- Threshold alerts
- Weekly summaries

## Interactive API Docs

Visit http://localhost:8000/docs for Swagger UI documentation with interactive API testing.
