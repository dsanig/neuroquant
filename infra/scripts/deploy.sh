#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
COMPOSE_FILES=( -f compose.yaml -f compose.production.yaml )

log() {
  echo "[deploy] $*"
}

usage() {
  cat <<USAGE
Usage: $0 [--build-only] [--skip-build] [--skip-migrate] [--skip-health]

Options:
  --build-only    Build images and exit.
  --skip-build    Skip image build and only start/reconcile services.
  --skip-migrate  Skip alembic migrations.
  --skip-health   Skip post-deploy health checks.
USAGE
}

BUILD_ONLY=0
SKIP_BUILD=0
SKIP_MIGRATE=0
SKIP_HEALTH=0

for arg in "$@"; do
  case "$arg" in
    --build-only) BUILD_ONLY=1 ;;
    --skip-build) SKIP_BUILD=1 ;;
    --skip-migrate) SKIP_MIGRATE=1 ;;
    --skip-health) SKIP_HEALTH=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      echo "[deploy] Unknown option: $arg" >&2
      usage
      exit 1
      ;;
  esac
done

cd "$REPO_DIR"

for env_file in .env backend/.env frontend/.env.local infra/.env; do
  if [[ ! -f "$env_file" ]]; then
    echo "[deploy] Missing required env file: $env_file" >&2
    exit 1
  fi
done

if [[ "$SKIP_BUILD" -eq 0 ]]; then
  log "Building images"
  docker compose "${COMPOSE_FILES[@]}" build
fi

if [[ "$BUILD_ONLY" -eq 1 ]]; then
  log "Build-only run complete"
  exit 0
fi

log "Starting and reconciling services"
docker compose "${COMPOSE_FILES[@]}" up -d

if [[ "$SKIP_MIGRATE" -eq 0 ]]; then
  log "Running alembic migrations in backend"
  docker compose "${COMPOSE_FILES[@]}" run --rm backend alembic upgrade head
fi

if [[ "$SKIP_HEALTH" -eq 0 ]]; then
  log "Running health checks"
  "$REPO_DIR/infra/scripts/health.sh"
fi

log "Deployment complete"
