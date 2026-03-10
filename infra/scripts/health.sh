#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
COMPOSE_FILES=( -f compose.yaml -f compose.production.yaml )

log() {
  echo "[health] $*"
}

cd "$REPO_DIR"
source .env

log "Container status"
docker compose "${COMPOSE_FILES[@]}" ps

log "Database connectivity"
docker compose "${COMPOSE_FILES[@]}" exec -T db \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT 1;'

log "API readiness through nginx"
curl -fsS http://127.0.0.1/healthz >/dev/null
curl -fsS http://127.0.0.1/api/v1/health >/dev/null

log "Frontend reachability"
curl -fsSI http://127.0.0.1/ >/dev/null

log "Worker and scheduler process checks"
docker compose "${COMPOSE_FILES[@]}" exec -T worker pgrep -fa 'celery.*worker'
docker compose "${COMPOSE_FILES[@]}" exec -T scheduler pgrep -fa 'celery.*beat'

log "Recent backend/task logs"
docker compose "${COMPOSE_FILES[@]}" logs --tail=20 backend worker scheduler

log "All checks passed"
