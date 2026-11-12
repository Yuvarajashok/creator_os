# Testing and known limitations

[Back to README](../README.md)

Status is based on static source inspection, not executed application tests.

## Known blockers and mismatches

| Area | Evidence and implication |
| --- | --- |
| ORM model | backend/models/intelligence_score.py defines metadata as a declarative attribute; this conflicts with SQLAlchemy's reserved metadata name and is a startup blocker to resolve |
| Frontend container | Dockerfile's final stage is Nginx/port 80; Compose invokes npm and maps port 3000 |
| Worker/beat settings | Settings requires JWT_SECRET_KEY, but their Compose environment lists omit it |
| Local environment | Settings loads .env in the process working directory |
| Schema location | Migration is under supabase/migrations/, not backend/database/migrations/ |
| Dependencies | EmailStr needs email-validator; smoke script imports requests; neither is explicitly listed in backend/requirements.txt |
| Test collection | pytest.ini names tests/, but no backend/tests/ directory is committed |
| Frontend lint | A lint script exists but no ESLint configuration is committed |
| Instagram sync | tasks.py uses random metrics, not Instagram API calls |

These issues are documented, not fixed by this change.

## Smoke script

With a running development backend and synthetic seeded database, from backend/:

```text
python -m scripts.test_api
```

Install requests in the isolated test environment if needed. The script registers a test account, logs in using the demo account, lists pages, and requests intelligence.

Limits of this script:

- It changes the development database.
- It can skip intelligence when no page is found.
- Non-200 intelligence responses are printed rather than asserted as failures.
- Its top-level exception handler prints errors instead of forcing a failing process exit.
- Its success banner alone is therefore insufficient evidence that all routes pass.

Do not present pytest as a complete passing suite: the configured tests directory is absent and the smoke functions are not a self-contained pytest fixture suite.

## Frontend checks

From frontend/, npm ci and npm run build are the intended dependency/build checks. npm run lint may require recovering the missing ESLint configuration. No check was run for this documentation-only change.

## Acceptance work still needed

Record actual environment and results for startup, registration/login, user isolation, page/post validation, empty metrics, date windows, model persistence, task execution, duplicate daily metrics, backup recovery, and frontend navigation. Use synthetic data.

Evaluate prediction performance on held-out time periods and distinguish heuristic labels from observed future outcomes. No accuracy metric is supplied.

The /health endpoint is not a dependency readiness probe. Successful /health responses do not prove migrations, Redis, worker tasks, or intelligence persistence are functioning.
