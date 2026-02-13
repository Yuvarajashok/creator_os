# Creator OS Architecture

## System Overview

Creator OS is a full-stack AI-powered Instagram growth intelligence platform that analyzes creator data and provides strategic recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    React + TypeScript                        │
│                      + TailwindCSS                          │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/REST
┌─────────────────▼───────────────────────────────────────────┐
│                      Backend API                             │
│                  FastAPI (Python 3.11)                      │
│  ┌──────────────┬──────────────┬────────────────────────┐  │
│  │ Auth Routes  │ Page Routes  │ Intelligence Routes    │  │
│  └──────────────┴──────────────┴────────────────────────┘  │
└─────────┬──────────────────┬────────────────┬──────────────┘
          │                  │                │
          │                  │                │
┌─────────▼──────┐  ┌───────▼───────┐  ┌────▼──────────────┐
│   PostgreSQL   │  │     Redis     │  │   Celery Workers  │
│   (Supabase)   │  │   (Cache +    │  │  - Data Sync      │
│  - Users       │  │    Broker)    │  │  - Intelligence   │
│  - Pages       │  └───────────────┘  │  - ML Training    │
│  - Posts       │                     └───────────────────┘
│  - Metrics     │
│  - Intel Scores│
└────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Intelligence Engine                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Signal Computation                                   │  │
│  │  - Posting Consistency                                │  │
│  │  - Reach Trend                                        │  │
│  │  - Conversion Health                                  │  │
│  │  - Momentum                                           │  │
│  │  - Engagement Stability                               │  │
│  │  - Viral Probability (ML)                             │  │
│  │  - Content Fatigue                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Weighted Scoring Model                               │  │
│  │  → Overall Score (0-100)                              │  │
│  │  → Growth Stage Classification                        │  │
│  │  → Strategic Recommendations                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Layer

**Technology**: React 18, TypeScript, TailwindCSS, Vite

**Components**:
- **Authentication**: Login, Register, Protected Routes
- **Pages Management**: List, Create, View pages
- **Dashboard**: Intelligence visualization with charts
- **Posts View**: Post listing with metrics
- **Layout**: Navigation, headers, common UI

**State Management**:
- React Context for authentication
- Local state for component data
- Axios for API communication

**Key Features**:
- JWT token management
- Responsive design
- Real-time data visualization (Recharts)
- Error handling and loading states

### Backend Layer

**Technology**: FastAPI (async), Python 3.11, SQLAlchemy

**Core Modules**:

1. **Authentication**
   - JWT token generation
   - Password hashing (bcrypt)
   - User registration and login
   - Protected route middleware

2. **API Routes**
   - `/api/v1/auth/*` - Authentication endpoints
   - `/api/v1/pages/*` - Page CRUD operations
   - `/api/v1/posts/*` - Post CRUD operations
   - `/api/v1/intelligence/*` - Intelligence score computation

3. **Database Models**
   - User: Authentication and profile
   - Page: Instagram page data
   - Post: Individual post metrics
   - DailyMetric: Daily aggregated metrics
   - IntelligenceScore: Computed scores and recommendations

### Intelligence Engine

**Purpose**: Compute growth intelligence from multi-signal analysis

**Signal Computation**:

1. **Posting Consistency** (Weight: 10%)
   - Analyzes posting frequency
   - Measures regularity of posting schedule
   - Compares to optimal posting rate (3-5x/week)

2. **Reach Trend** (Weight: 15%)
   - Tracks reach growth over time
   - Compares first-half vs second-half performance
   - Identifies growth or decline patterns

3. **Conversion Health** (Weight: 15%)
   - Profile visits / reach ratio
   - Measures content-to-profile conversion
   - Indicates CTA effectiveness

4. **Momentum** (Weight: 20%)
   - Follower growth rate
   - Daily growth velocity
   - Acceleration/deceleration detection

5. **Engagement Stability** (Weight: 10%)
   - Coefficient of variation in engagement rates
   - Consistency across posts
   - Audience retention indicator

6. **Viral Probability** (Weight: 20%)
   - ML-based prediction using RandomForest
   - Trained on historical post performance
   - Features: post type, timing, caption length, engagement

7. **Content Fatigue** (Weight: -10%, penalty)
   - Declining engagement trend detection
   - Recent performance degradation
   - Audience saturation indicator

**Weighted Score Formula**:
```
Score = (PC × 0.10) + (RT × 0.15) + (CH × 0.15) +
        (M × 0.20) + (ES × 0.10) + (VP × 0.20) -
        (CF × 0.10)
```

**Growth Stage Classification**:
- 80-100: Dominant Growth
- 60-79: Stable Growth
- 40-59: At Risk
- 0-39: Critical

**Recommendation Engine**:
- Rule-based recommendations
- Triggered by weak signals
- Actionable strategic guidance

### AI/ML Component

**Virality Predictor**:

**Algorithm**: Random Forest Regressor

**Features**:
- Hour of day
- Day of week
- Post type (image/video/carousel/reel)
- Caption length
- Like count
- Comment count
- Save count
- Share count

**Training**:
- Requires minimum 10 posts
- Auto-retraining every 30 days
- Triggered when data doubles

**Prediction**:
- Outputs virality probability (0-1)
- Averaged across recent 5 posts
- Normalized to 0-100 scale

**Model Storage**:
- Pickle serialization
- Per-page model files
- Located in `/models` directory

### Background Tasks (Celery)

**Broker**: Redis

**Tasks**:

1. **Daily Instagram Sync** (24h interval)
   - Mock data generation for demo
   - Real Instagram API integration ready
   - Updates follower counts, metrics

2. **Weekly Intelligence Summary** (7d interval)
   - Generates reports for all pages
   - Email/notification ready

3. **Model Retraining** (7d interval)
   - Checks if retraining needed
   - Trains virality models
   - Updates predictions

**Scheduler**: Celery Beat
- Cron-like task scheduling
- Distributed task execution
- Result backend for monitoring

### Data Layer

**Database**: PostgreSQL (via Supabase)

**Schema**:

```sql
users
├── id (uuid, pk)
├── email (text, unique)
├── full_name (text)
├── hashed_password (text)
├── role (text)
└── is_active (boolean)

pages
├── id (uuid, pk)
├── user_id (uuid, fk)
├── instagram_username (text, unique)
├── follower_count (int)
├── post_count (int)
└── last_synced_at (timestamp)

posts
├── id (uuid, pk)
├── page_id (uuid, fk)
├── instagram_post_id (text, unique)
├── post_type (text)
├── timestamp (timestamp)
├── like_count (int)
├── reach (int)
└── engagement_rate (numeric)

daily_metrics
├── id (uuid, pk)
├── page_id (uuid, fk)
├── date (date)
├── follower_count (int)
├── impressions (int)
└── profile_visits (int)

intelligence_scores
├── id (uuid, pk)
├── page_id (uuid, fk)
├── overall_score (numeric)
├── signals (jsonb)
├── recommendations (jsonb)
└── created_at (timestamp)
```

**Row Level Security (RLS)**:
- All tables have RLS enabled
- Users can only access their own data
- Policies enforce data isolation

### Caching Layer

**Technology**: Redis

**Usage**:
- Session storage
- Celery broker
- Task result backend
- Future: API response caching

### Deployment

**Containerization**: Docker + Docker Compose

**Services**:
- `backend`: FastAPI application
- `celery_worker`: Background task processor
- `celery_beat`: Task scheduler
- `frontend`: React application
- `redis`: Cache and message broker

**Production Deployment Options**:
1. Render (recommended for beginners)
2. Railway (easy one-click deploy)
3. DigitalOcean App Platform (scalable)
4. AWS/GCP/Azure (enterprise)

## Data Flow

### Intelligence Score Generation

```
1. User requests intelligence score
   ↓
2. API validates authentication
   ↓
3. Engine fetches page data
   ↓
4. Fetch posts (last 30 days)
   ↓
5. Fetch daily metrics (last 30 days)
   ↓
6. Compute 7 signals in parallel
   ↓
7. Calculate weighted overall score
   ↓
8. Classify growth stage
   ↓
9. Generate recommendations
   ↓
10. Store in database
   ↓
11. Return JSON response
```

### ML Virality Prediction

```
1. Intelligence engine needs viral probability
   ↓
2. Load existing model (if available)
   ↓
3. If no model or outdated:
   ├─ Extract features from posts
   ├─ Calculate virality scores
   ├─ Train RandomForest model
   └─ Save model to disk
   ↓
4. Extract features from recent posts
   ↓
5. Predict virality for each
   ↓
6. Average predictions
   ↓
7. Return probability (0-100)
```

## Security

**Authentication**:
- JWT tokens (HS256)
- 30-minute expiration
- Secure password hashing (bcrypt)

**Authorization**:
- Role-based access control
- RLS at database level
- API endpoint protection

**Data Protection**:
- HTTPS in production
- Environment variable secrets
- No hardcoded credentials

## Scalability

**Horizontal Scaling**:
- Stateless backend (scales with load balancer)
- Multiple Celery workers
- Redis cluster for high availability

**Vertical Scaling**:
- Increase container resources
- Database connection pooling
- Optimize queries

**Performance Optimizations**:
- Database indexing on key fields
- Async/await throughout backend
- Lazy loading in frontend
- API response pagination (future)

## Monitoring

**Logs**:
- Structured logging throughout
- CloudWatch/Datadog integration ready
- Error tracking

**Metrics**:
- API response times
- Celery task execution
- Database query performance
- Error rates

## Future Enhancements

1. **Real Instagram API Integration**
   - OAuth authentication
   - Automated data sync
   - Real-time webhook events

2. **Advanced Analytics**
   - Competitor analysis
   - Hashtag performance
   - Best posting times

3. **Notifications**
   - Email alerts for score changes
   - Weekly summary reports
   - Threshold notifications

4. **Multi-Platform**
   - TikTok integration
   - YouTube analytics
   - Twitter/X metrics

5. **Team Features**
   - Multi-user pages
   - Role permissions
   - Collaborative dashboards

6. **Export/Reporting**
   - PDF report generation
   - CSV data export
   - Custom date ranges
