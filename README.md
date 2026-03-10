# Investment Control Center

Production-minded self-hosted internal hedge fund operating platform for portfolio control, risk, margin, trade history, and auditability.

## Monorepo layout

- `frontend/` - Next.js TypeScript authenticated application shell
- `backend/` - FastAPI + SQLAlchemy + Alembic + Celery services
- `infra/` - Nginx reverse proxy and monitoring scaffolding
- `docs/` - architecture and operational documentation

## Prerequisites

- Docker Engine 24+
- Docker Compose v2
- GNU Make

## Quick start (development)

1. Copy environment templates:
   ```bash
   cp .env.example .env
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local
   cp infra/.env.example infra/.env
   ```
2. Build and start stack:
   ```bash
   make up
   ```
3. Run migrations:
   ```bash
   make migrate
   ```
4. Seed sample data:
   ```bash
   make seed
   ```
5. Access services:
   - Frontend: http://localhost:3000
   - API docs: http://localhost:8000/docs
   - Nginx gateway: http://localhost:8080

## Production deployment (Debian VM)

1. Install Docker/Compose and clone repo.
2. Provide secure `.env` values (never commit secrets).
3. Build and start:
   ```bash
   docker compose -f compose.yaml -f compose.production.yaml up -d --build
   ```
4. Run one-time migration job:
   ```bash
   docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
   ```
5. Optional seed (non-production only):
   ```bash
   docker compose -f compose.yaml -f compose.production.yaml run --rm backend python -m app.seed
   ```

## Common commands

```bash
make up            # start local stack
make down          # stop stack
make logs          # tail logs
make test          # backend tests
make lint          # backend + frontend lint
make migrate       # alembic upgrade
make seed          # load sample records
```

## Security & auth notes

- Session/JWT hybrid internal auth with RBAC claims.
- HTTPOnly secure cookies in production.
- API namespaced at `/api/v1`.

See `docs/architecture.md` and `TODO.md` for implementation details and roadmap.
