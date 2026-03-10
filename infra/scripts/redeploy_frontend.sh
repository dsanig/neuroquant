#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)

cd "$ROOT_DIR"

echo "[frontend] Building frontend image"
docker compose "${COMPOSE_ARGS[@]}" build frontend

echo "[frontend] Restarting frontend and nginx"
docker compose "${COMPOSE_ARGS[@]}" up -d frontend nginx

echo "[frontend] Validating health"
"$ROOT_DIR/infra/scripts/check_health.sh"
