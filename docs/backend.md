# Investment Control Center Backend

Production-oriented FastAPI backend for a hedge fund derivatives control platform.

## Stack
- FastAPI + Pydantic v2
- SQLAlchemy 2.x + Alembic
- PostgreSQL
- Redis + Celery

## Layering
- `routers/` API transport only
- `repositories/` SQL/data access
- `services/` deterministic business logic
- `schemas/` IO contracts
- `models/` relational domain model
- `tasks/` async jobs and task history persistence hooks

## API v1 endpoints
- `/api/v1/auth/login`
- `/api/v1/auth/me`
- `/api/v1/dashboard/summary`
- `/api/v1/positions`
- `/api/v1/trades`
- `/api/v1/trades/detect-rolls`
- `/api/v1/strategies`
- `/api/v1/risk/summary`
- `/api/v1/margin/summary`
- `/api/v1/performance/summary`
- `/api/v1/income`
- `/api/v1/imports`
- `/api/v1/audit-log`
- `/api/v1/health`

## Security baseline
- JWT login with hashed passwords
- `auth/me` identity endpoint
- RBAC guard helper (`require_roles`) for role-gated endpoints

## Operational principles
- structured logging via `structlog`
- explicit exception surfaces (`HTTPException`)
- no router-level business logic
- metric source attribution (`broker` vs `app`) at storage level
