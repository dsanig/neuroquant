# Investment Control Center Deployment (Debian + Docker Compose)

## 1. Prepare host and code

```bash
sudo mkdir -p /srv/investment-control-center
sudo chown -R "$USER":"$USER" /srv/investment-control-center
git clone <REPO_URL> /srv/investment-control-center
cd /srv/investment-control-center
```

## 2. Copy environment templates

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
cp infra/.env.example infra/.env
chmod 600 .env backend/.env frontend/.env.local infra/.env
```

## 3. Set secrets and endpoints

Edit files with concrete values:

```bash
nano .env
nano backend/.env
nano frontend/.env.local
nano infra/.env
```

Minimum required values:

- `.env`: `POSTGRES_PASSWORD`, `JWT_SECRET_KEY`
- `backend/.env`: `DATABASE_URL`, `JWT_SECRET_KEY`
- `frontend/.env.local`: `NEXT_PUBLIC_API_BASE_URL`
- `infra/.env`: `GRAFANA_ADMIN_PASSWORD` (if using monitoring)

## 4. Build images

```bash
./infra/scripts/deploy.sh --build-only
```

Equivalent raw command:

```bash
docker compose -f compose.yaml -f compose.production.yaml build
```

## 5. Start stack

```bash
./infra/scripts/deploy.sh
```

Equivalent raw command:

```bash
docker compose -f compose.yaml -f compose.production.yaml up -d
```

## 6. Run database migrations

```bash
docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
```

## 7. Validate deployment

```bash
./infra/scripts/check_health.sh
```

Manual checks:

```bash
# DB connectivity
docker compose -f compose.yaml -f compose.production.yaml exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT 1;'

# API health (through nginx)
curl -fsS http://127.0.0.1/api/v1/health
curl -fsS http://127.0.0.1/healthz

# Frontend reachability
curl -fsSI http://127.0.0.1/

# Worker and scheduler process checks
docker compose -f compose.yaml -f compose.production.yaml exec -T worker pgrep -fa 'celery.*worker'
docker compose -f compose.yaml -f compose.production.yaml exec -T scheduler pgrep -fa 'celery.*beat'
```

## 8. Read logs

```bash
docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200
docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200 backend
docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200 worker scheduler
```

## 9. Restart one service

```bash
docker compose -f compose.yaml -f compose.production.yaml restart backend
```

## 10. Rebuild one service only

```bash
# backend only
docker compose -f compose.yaml -f compose.production.yaml build backend
docker compose -f compose.yaml -f compose.production.yaml up -d backend

# frontend only
docker compose -f compose.yaml -f compose.production.yaml build frontend
docker compose -f compose.yaml -f compose.production.yaml up -d frontend nginx
```
