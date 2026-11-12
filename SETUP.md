# Creator OS setup

[README](README.md) · [Known issues](docs/TESTING_AND_LIMITATIONS.md)

## Read this first

This guide explains the intended setup and known blockers. It does not certify a successful launch. Resolve the documented source/configuration blockers separately before treating the commands as a working quick start.

The backend Dockerfile targets Python 3.11 and the frontend Dockerfile targets Node 18. These are repository targets, not a statement about current vendor support. Use an isolated development environment and a disposable database.

## Clone and configuration

```text
git clone https://github.com/Yuvarajashok/creator_os.git
cd creator_os
```

Copy .env.example to a local .env and replace placeholders. Never commit the filled-in file.

| Setting | Purpose |
| --- | --- |
| SECRET_KEY, JWT_SECRET_KEY | Required application/signing secrets |
| SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY | Required by Settings |
| DATABASE_URL | PostgreSQL connection; database.py converts postgresql:// to postgresql+asyncpg:// |
| REDIS_URL | Redis address |
| CELERY_BROKER_URL, CELERY_RESULT_BACKEND | Celery transport and results |
| BACKEND_CORS_ORIGINS | JSON array of allowed frontend origins |
| ENVIRONMENT, DEBUG | Runtime environment and logging/debug configuration |
| AI_MODEL_PATH | Directory for generated model/scaler artifacts |
| MIN_POSTS_FOR_TRAINING | Predictor threshold, default 10 |

Generate secret values locally and paste literal values into the configuration. A .env file does not execute shell command substitution.

Settings reads .env relative to the current working directory. When running commands from backend/, provide backend/.env or export the required variables into that terminal. A root .env alone is used by Compose interpolation, not automatically by a Python process started inside backend/.

Keep backend secrets out of frontend configuration. The frontend reads VITE_API_URL, defaulting to http://localhost:8000.

## Database

The committed schema is [supabase/migrations/20260213090602_create_creator_os_schema.sql](supabase/migrations/20260213090602_create_creator_os_schema.sql). Review it and apply it to an isolated Supabase development database; no migration has been applied on your behalf. There is no backend/database/migrations/ directory.

Confirm tables and model compatibility before running seed scripts. RLS in a migration is not proof of end-to-end user isolation through the application's direct database connection.

## Local processes

After resolving known blockers, from backend/:

```text
python -m venv .venv
```

Activate it using .venv/bin/activate on POSIX or .\.venv\Scripts\Activate.ps1 in PowerShell, then:

```text
python -m pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

EmailStr needs email-validator, which is not explicitly listed in requirements.txt. If the dependency is missing, install it in the local environment and record the version used. Do not infer a tested dependency set from installation alone.

From frontend/ in another terminal:

```text
npm ci
npm run dev
```

Vite is configured on port 3000. Provide VITE_API_URL in frontend/.env.local when using a different API address. Permit the matching origin in BACKEND_CORS_ORIGINS.

Redis, the worker, and the scheduler are separate processes. Intended commands from backend/, with the same required environment:

```text
celery -A background_tasks.celery_app worker --loglevel=info
celery -A background_tasks.celery_app beat --loglevel=info
```

Use only synthetic data with the scheduler: the sync task mutates metrics using random numbers.

## Docker limitations

The committed Compose configuration is not a verified one-command startup:

- frontend/Dockerfile ends in an Nginx image listening on port 80, but Compose overrides it with npm run dev and maps 3000:3000.
- Worker and beat environment lists omit required JWT_SECRET_KEY.
- Backend reload mode and bind mounts describe development, not production.

Those files are deliberately not changed by this documentation work. Repair them in a separate implementation task before relying on Compose.

## Demo data and checking

Once the backend imports and database work, run from backend/:

```text
python -m scripts.seed_data
```

It writes a synthetic demo account, page, 30 posts, and 30 daily metrics. Demo credentials are demo@creatoros.com / demo123456; use them only in a disposable development environment. An existing demo account makes the script skip seeding, so rerunning does not necessarily repair a partial seed.

See [testing](docs/TESTING_AND_LIMITATIONS.md) for the smoke script and its limits.
