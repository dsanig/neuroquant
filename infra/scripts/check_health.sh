#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)

cd "$ROOT_DIR"
source .env

echo "[health] Container status"
docker compose "${COMPOSE_ARGS[@]}" ps

echo "[health] Database connectivity"
docker compose "${COMPOSE_ARGS[@]}" exec -T db \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT 1;'

echo "[health] API readiness"
curl -fsS http://127.0.0.1/healthz >/dev/null
curl -fsS http://127.0.0.1/api/v1/health >/dev/null

echo "[health] Frontend reachability"
curl -fsSI http://127.0.0.1/ >/dev/null

echo "[health] Worker process"
docker compose "${COMPOSE_ARGS[@]}" exec -T worker pgrep -fa 'celery.*worker'

echo "[health] Scheduler process"
docker compose "${COMPOSE_ARGS[@]}" exec -T scheduler pgrep -fa 'celery.*beat'

echo "[health] Worker and scheduler recent logs"
docker compose "${COMPOSE_ARGS[@]}" logs --tail=20 worker scheduler

echo "[health] OK"
