# Creator OS Deployment Guide

This guide covers deploying Creator OS to various platforms.

## Prerequisites

- Docker installed
- Supabase account with database configured
- Redis instance (can use Docker or cloud provider)

## Environment Configuration

Create a `.env` file with the following variables:

```bash
# Backend Configuration
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key-min-32-chars

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
DATABASE_URL=postgresql://postgres:[password]@[host]:[port]/postgres

# Redis Configuration (use your cloud Redis URL)
REDIS_URL=redis://your-redis-host:6379/0

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.com"]

# Celery Configuration
CELERY_BROKER_URL=redis://your-redis-host:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/0
```

## Render Deployment

### Backend Service

1. Create new Web Service
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Environment**: Add all variables from `.env`
   - **Health Check Path**: `/health`

### Celery Worker

1. Create new Background Worker
2. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A background_tasks.celery_app worker --loglevel=info`
   - **Environment**: Same as backend

### Celery Beat Scheduler

1. Create new Background Worker
2. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A background_tasks.celery_app beat --loglevel=info`
   - **Environment**: Same as backend

### Frontend Service

1. Create new Static Site
2. Configure:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
   - **Environment Variables**:
     - `VITE_API_URL=https://your-backend.onrender.com`

## Railway Deployment

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login and initialize:
```bash
railway login
railway init
```

3. Deploy:
```bash
railway up
```

4. Set environment variables in Railway dashboard

## DigitalOcean App Platform

1. Connect your GitHub repository
2. Configure components:

**Backend API**:
- Type: Web Service
- Dockerfile: `backend/Dockerfile`
- HTTP Port: 8000
- Environment variables from `.env`

**Celery Worker**:
- Type: Worker
- Dockerfile: `backend/Dockerfile`
- Run Command: `celery -A background_tasks.celery_app worker --loglevel=info`

**Frontend**:
- Type: Static Site
- Dockerfile: `frontend/Dockerfile`
- Environment: `VITE_API_URL`

## Docker Compose Production

For self-hosted deployment:

1. Update `docker-compose.yml` for production
2. Add production environment variables
3. Use production-ready PostgreSQL and Redis
4. Deploy:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Redis Setup

### Redis Cloud (Recommended)

1. Sign up at https://redis.com/try-free/
2. Create a database
3. Copy the connection URL
4. Update `REDIS_URL` in your environment

### Railway Redis

```bash
railway add redis
```

### Render Redis

Create a Redis instance in Render dashboard.

## Database Migration

Your Supabase database should already have the schema applied. If deploying fresh:

1. Go to Supabase Dashboard
2. SQL Editor
3. Run the migration from `backend/database/migrations/`

## Health Checks

- Backend: `GET /health`
- Expected response: `{"status": "healthy", "environment": "production", "version": "1.0.0"}`

## Monitoring

### Logs

**Render**:
- View logs in the dashboard

**Railway**:
```bash
railway logs
```

**Docker**:
```bash
docker-compose logs -f
```

### Performance

- Monitor API response times
- Check Celery task execution
- Monitor Redis memory usage
- Track database query performance

## Troubleshooting

### Backend not starting

1. Check environment variables are set
2. Verify database connection
3. Check Redis connectivity
4. Review logs for errors

### Celery tasks not running

1. Verify Redis connection
2. Check Celery worker logs
3. Ensure broker URL is correct
4. Verify beat scheduler is running

### Frontend can't connect to API

1. Check CORS configuration
2. Verify API URL in frontend environment
3. Check network connectivity
4. Review browser console for errors

## Security Checklist

- [ ] Change all default secrets
- [ ] Use strong JWT secret
- [ ] Enable HTTPS
- [ ] Configure proper CORS origins
- [ ] Secure Redis with password
- [ ] Use Supabase RLS policies
- [ ] Enable rate limiting
- [ ] Set up monitoring alerts
- [ ] Regular security updates
- [ ] Backup database regularly

## Scaling

### Horizontal Scaling

- Add more backend instances
- Scale Celery workers based on load
- Use Redis cluster for high availability

### Vertical Scaling

- Increase container resources
- Optimize database queries
- Use connection pooling

## Backup Strategy

1. **Database**: Supabase automatic backups
2. **Redis**: Use Redis persistence (RDB/AOF)
3. **ML Models**: Store in cloud storage
4. **Environment configs**: Secure vault

## Cost Optimization

- Use appropriate instance sizes
- Enable auto-scaling
- Monitor resource usage
- Optimize database queries
- Cache frequently accessed data
- Use CDN for frontend assets

## Support

For issues:
1. Check logs
2. Review this guide
3. Check GitHub issues
4. Contact support

---

**Note**: Always test in staging before deploying to production.
