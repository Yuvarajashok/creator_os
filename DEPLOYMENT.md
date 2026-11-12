# Deployment considerations

[README](README.md) · [Setup](SETUP.md) · [Known issues](docs/TESTING_AND_LIMITATIONS.md)

No deployment was performed or verified for this documentation update. Resolve the known ORM and container/environment blockers, then validate in staging before exposing the application.

## Service layout

- Backend: working directory backend/, dependencies from requirements.txt.
- Frontend: working directory frontend/, npm ci followed by npm run build; output dist/.
- Celery worker and beat: backend environment and Redis connectivity.
- PostgreSQL: reviewed schema from supabase/migrations/.
- Persistent model directory: AI_MODEL_PATH for generated per-page models/scalers.

The repository does not contain docker-compose.prod.yml. Do not run an example referring to that nonexistent file. The existing docker-compose.yml uses development commands and has the mismatches described in SETUP.md.

## Frontend configuration

VITE_API_URL must point to the reachable backend when building the frontend. Vite embeds this configuration in built assets; setting a variable only after an Nginx image is built does not rewrite its JavaScript.

Serve dist/ with SPA navigation fallback. The provided frontend image serves Nginx on port 80, unlike the development server's port 3000.

## Backend configuration

Provide all required settings to API, worker, and scheduler processes. Use dedicated secrets, appropriate CORS origins, HTTPS, and restricted database/Redis access. Validate authentication and cross-user ownership with actual tests.

The /health route returns a process-level status payload; it does not perform database or Redis readiness checks.

## Data protection and operation

- Keep .env files, real credentials, database exports, user data, and generated model artifacts out of Git.
- Disable mock sync for real datasets; the current task generates random metrics.
- Back up the database and model artifacts privately; test recovery into an isolated environment.
- Confirm the actual database provider's backup/retention settings instead of assuming automatic backups exist.
- Run only one intended beat schedule to avoid duplicate jobs.
- Record dependency/build versions, deployment configuration, and validation results for reproducibility.
- A trained artifact should come from a trusted source; loading arbitrary serialized models is not a data-import feature.

Provider-specific pricing, dashboards, and deployment recipes are not verified here. The deployment target must be configured and tested separately.
