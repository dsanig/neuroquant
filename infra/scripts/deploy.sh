#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)

usage() {
  cat <<USAGE
Usage: $0 [--build-only] [--skip-migrate]

Options:
  --build-only    Build all images and exit.
  --skip-migrate  Do not run alembic migrations.
USAGE
}

BUILD_ONLY=0
SKIP_MIGRATE=0

for arg in "$@"; do
  case "$arg" in
    --build-only) BUILD_ONLY=1 ;;
    --skip-migrate) SKIP_MIGRATE=1 ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

cd "$ROOT_DIR"

for env_file in .env backend/.env frontend/.env.local infra/.env; do
  if [[ ! -f "$env_file" ]]; then
    echo "Missing $env_file. Copy templates before deploy:"
    echo "  cp .env.example .env"
    echo "  cp backend/.env.example backend/.env"
    echo "  cp frontend/.env.example frontend/.env.local"
    echo "  cp infra/.env.example infra/.env"
    exit 1
  fi
done

echo "[deploy] Building images"
docker compose "${COMPOSE_ARGS[@]}" build

if [[ "$BUILD_ONLY" -eq 1 ]]; then
  echo "[deploy] Build complete (--build-only)."
  exit 0
fi

echo "[deploy] Starting stack"
docker compose "${COMPOSE_ARGS[@]}" up -d

if [[ "$SKIP_MIGRATE" -eq 0 ]]; then
  echo "[deploy] Running alembic migrations"
  docker compose "${COMPOSE_ARGS[@]}" run --rm backend alembic upgrade head
fi

echo "[deploy] Running health checks"
"$ROOT_DIR/infra/scripts/check_health.sh"

echo "[deploy] Complete"
