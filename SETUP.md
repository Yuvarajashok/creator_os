# Creator OS - Complete Setup Guide

This guide will help you set up and run Creator OS locally.

## Prerequisites

Before you begin, ensure you have:

- **Docker & Docker Compose** (v20.10+)
- **Node.js** (v18+)
- **Python** (v3.11+)
- **Supabase Account** (free tier works)
- **Git**

## Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd creator-os
```

## Step 2: Supabase Setup

### 2.1 Create Supabase Project

1. Go to https://supabase.com
2. Sign up/Login
3. Create a new project
4. Wait for project to initialize (2-3 minutes)

### 2.2 Get Credentials

From your Supabase dashboard:

1. Go to **Settings** → **API**
2. Copy:
   - Project URL (SUPABASE_URL)
   - anon/public key (SUPABASE_ANON_KEY)
   - service_role key (SUPABASE_SERVICE_KEY)

3. Go to **Settings** → **Database**
4. Copy connection string (DATABASE_URL)
   - Format: `postgresql://postgres:[password]@[host]:[port]/postgres`

### 2.3 Run Database Migration

The migration has already been applied to your Supabase database. Verify by going to:
- Supabase Dashboard → **Database** → **Tables**
- You should see: users, pages, posts, daily_metrics, intelligence_scores

If tables don't exist, go to **SQL Editor** and run the migration SQL.

## Step 3: Environment Configuration

### 3.1 Create .env File

```bash
cp .env.example .env
```

### 3.2 Update .env with Your Credentials

```bash
# Use your Supabase credentials
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
DATABASE_URL=postgresql://postgres:[password]@[host]:[port]/postgres

# Generate secure keys (32+ characters)
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)

# Keep these as-is for local development
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Step 4: Start Services with Docker

### 4.1 Start All Services

```bash
docker-compose up -d
```

This will start:
- Redis (port 6379)
- Backend API (port 8000)
- Celery Worker
- Celery Beat Scheduler
- Frontend (port 3000)

### 4.2 Verify Services

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f
```

Expected output:
```
creator_os_backend    | INFO: Application startup complete
creator_os_frontend   | VITE ready in X ms
creator_os_celery     | celery@hostname ready
creator_os_redis      | Ready to accept connections
```

## Step 5: Seed Demo Data

```bash
# Enter backend container
docker-compose exec backend bash

# Run seed script
python scripts/seed_data.py

# Exit container
exit
```

This creates:
- Demo user: `demo@creatoros.com` / `demo123456`
- Demo Instagram page with 30 posts
- 30 days of metrics data

## Step 6: Access Application

Open your browser:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Login

```
Email: demo@creatoros.com
Password: demo123456
```

## Step 7: Verify Intelligence Engine

1. Login to the app
2. Click on the demo page
3. View the dashboard
4. You should see:
   - Intelligence Score (0-100)
   - Growth Stage
   - Signal breakdown charts
   - Strategic recommendations
   - Key metrics

## Local Development (Without Docker)

If you prefer to run services individually:

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (separate terminal)
redis-server

# Start Celery worker (separate terminal)
celery -A background_tasks.celery_app worker --loglevel=info

# Start Celery beat (separate terminal)
celery -A background_tasks.celery_app beat --loglevel=info

# Start FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Testing

### Test Backend API

```bash
cd backend
python scripts/test_api.py
```

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "1.0.0"
}
```

### Test Intelligence API

```bash
# First, get access token by logging in
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@creatoros.com&password=demo123456"

# Use the token to get intelligence score
curl -X GET "http://localhost:8000/api/v1/intelligence/{page_id}" \
  -H "Authorization: Bearer {your_token}"
```

## Troubleshooting

### Backend won't start

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
- Check DATABASE_URL is correct
- Verify Supabase project is active
- Check network connectivity

### Celery worker issues

**Error**: `Error: No nodes replied within time constraint`

**Solution**:
- Ensure Redis is running: `docker-compose ps redis`
- Check REDIS_URL in .env
- Restart services: `docker-compose restart`

### Frontend can't reach API

**Error**: `Network Error` or `CORS error`

**Solution**:
- Check backend is running on port 8000
- Verify BACKEND_CORS_ORIGINS in .env includes `http://localhost:3000`
- Check browser console for errors

### No intelligence data

**Issue**: Dashboard shows 0 score or insufficient data

**Solution**:
- Run seed script: `python scripts/seed_data.py`
- Ensure posts have metrics (reach, impressions > 0)
- Check page has at least 10 posts

### Docker issues

**Error**: `Cannot connect to Docker daemon`

**Solution**:
- Start Docker Desktop
- Verify Docker is running: `docker ps`

**Error**: `Port already in use`

**Solution**:
```bash
# Find process using port
lsof -i :8000  # or :3000, :6379

# Kill process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Stop Services

```bash
docker-compose down
```

### Rebuild After Code Changes

```bash
docker-compose down
docker-compose build
docker-compose up -d
```

### Access Database

```bash
# Via Supabase Dashboard
# Go to: Database → Table Editor

# Or use psql
psql "postgresql://postgres:[password]@[host]:[port]/postgres"
```

### Reset Database

```bash
# Drop all tables in Supabase Dashboard
# Then re-run migration from SQL Editor
# Then seed data again
```

## Project Structure

```
creator-os/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── core/                      # Config, security
│   ├── models/                    # SQLAlchemy models
│   ├── schemas/                   # Pydantic schemas
│   ├── routes/                    # API endpoints
│   ├── intelligence/              # Intelligence engine
│   ├── ai_engine/                 # ML virality predictor
│   ├── background_tasks/          # Celery tasks
│   └── scripts/                   # Seed & test scripts
├── frontend/
│   ├── src/
│   │   ├── pages/                 # React pages
│   │   ├── components/            # React components
│   │   ├── services/              # API client
│   │   └── context/               # Auth context
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## Next Steps

1. **Explore the Dashboard**: View intelligence scores and recommendations
2. **Add Your Own Page**: Create a new Instagram page
3. **Add Posts**: Manually or via API
4. **Monitor Background Tasks**: Check Celery logs for automated syncs
5. **Customize Intelligence Engine**: Modify weights in `intelligence/engine.py`
6. **Deploy to Production**: See DEPLOYMENT.md

## Support

- Check logs: `docker-compose logs -f`
- Review API docs: http://localhost:8000/docs
- Test API: `python scripts/test_api.py`

## Quick Reference

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| API Docs | 8000 | http://localhost:8000/docs |
| Redis | 6379 | redis://localhost:6379 |

| Command | Description |
|---------|-------------|
| `docker-compose up -d` | Start all services |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f` | View logs |
| `docker-compose restart` | Restart services |
| `python scripts/seed_data.py` | Add demo data |
| `python scripts/test_api.py` | Test API |

---

**You're all set!** 🚀

Login at http://localhost:3000 with `demo@creatoros.com` / `demo123456`
