# Creator OS - AI-Powered Instagram Growth Intelligence Platform

A complete production-ready SaaS platform that provides strategic recommendations for Instagram creators.

## Features

- **AI Intelligence Engine**: Strategic growth recommendations based on multi-signal analysis
- **Virality Predictor**: ML-powered prediction of post viral potential
- **Multi-User Support**: JWT authentication with role-based access
- **Page Management**: Manage multiple Instagram pages
- **Post Analytics**: Track engagement, reach, and conversion metrics
- **Background Tasks**: Automated data sync and intelligence generation
- **Real-time Dashboard**: React-based analytics visualization

## Tech Stack

### Backend
- FastAPI (async)
- PostgreSQL (via Supabase)
- Redis
- Celery
- SQLAlchemy
- Pydantic v2
- scikit-learn
- JWT authentication

### Frontend
- React 18
- TypeScript
- TailwindCSS
- Recharts
- Axios
- React Router

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Supabase account

### 1. Clone and Setup

```bash
# Copy environment variables
cp .env.example .env

# Edit .env with your Supabase credentials
```

### 2. Configure Supabase

Run the database migrations in your Supabase dashboard or use the Supabase CLI.

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 5. Create Test User

```bash
# Run seed data script
cd backend
python scripts/seed_data.py
```

Default test user:
- Email: demo@creatoros.com
- Password: demo123456

## Local Development (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (via Supabase)
# See database/migrations/

# Start Redis
redis-server

# Start Celery worker
celery -A background_tasks.celery_app worker --loglevel=info

# Start Celery beat
celery -A background_tasks.celery_app beat --loglevel=info

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## API Documentation

### Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"John Doe"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"password123"}'
```

### Intelligence API

```bash
# Get intelligence score
curl -X GET http://localhost:8000/api/v1/intelligence/{page_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Intelligence Engine

The system computes an overall intelligence score (0-100) using weighted signals:

- **Posting Consistency** (10%): Regular posting frequency
- **Reach Trend** (15%): Growth in impressions
- **Conversion Health** (15%): Profile visits from content
- **Momentum** (20%): Follower growth rate
- **Engagement Stability** (10%): Consistent interaction rates
- **Viral Probability** (20%): ML-predicted virality
- **Content Fatigue** (-10%): Penalty for declining performance

### Growth Stages

- **80-100**: Dominant Growth
- **60-79**: Stable Growth
- **40-59**: At Risk
- **0-39**: Critical

## Deployment

### Render

```bash
# Backend
- New Web Service
- Build Command: pip install -r requirements.txt
- Start Command: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
- New Static Site
- Build Command: npm install && npm run build
- Publish Directory: dist
```

### Railway

```bash
# Deploy with Railway CLI
railway up
```

### DigitalOcean App Platform

Use the included Dockerfiles for container deployment.

## Project Structure

```
creator-os/
├── backend/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── analytics/
│   ├── intelligence/
│   ├── ai_engine/
│   ├── background_tasks/
│   ├── services/
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── context/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Testing

```bash
# Backend tests
cd backend
pytest

# API validation
python scripts/test_api.py
```

## Environment Variables

See `.env.example` for all required configuration.

## License

MIT

## Support

For issues and questions, please open a GitHub issue.
