#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)

cd "$ROOT_DIR"

echo "[backend] Building backend image"
docker compose "${COMPOSE_ARGS[@]}" build backend

echo "[backend] Applying database migrations"
docker compose "${COMPOSE_ARGS[@]}" run --rm backend alembic upgrade head

echo "[backend] Restarting backend runtime services"
docker compose "${COMPOSE_ARGS[@]}" up -d backend worker scheduler

echo "[backend] Validating health"
"$ROOT_DIR/infra/scripts/check_health.sh"
