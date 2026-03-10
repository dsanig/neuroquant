#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
COMPOSE_FILES=( -f compose.yaml -f compose.production.yaml )
SKIP_MIGRATE=0

log() {
  echo "[rebuild-backend] $*"
}

for arg in "$@"; do
  case "$arg" in
    --skip-migrate) SKIP_MIGRATE=1 ;;
    -h|--help)
      echo "Usage: $0 [--skip-migrate]"
      exit 0
      ;;
    *)
      echo "[rebuild-backend] Unknown option: $arg" >&2
      exit 1
      ;;
  esac
done

cd "$REPO_DIR"

log "Building backend image"
docker compose "${COMPOSE_FILES[@]}" build backend

if [[ "$SKIP_MIGRATE" -eq 0 ]]; then
  log "Applying database migrations"
  docker compose "${COMPOSE_FILES[@]}" run --rm backend alembic upgrade head
fi

log "Restarting backend, worker, and scheduler"
docker compose "${COMPOSE_FILES[@]}" up -d backend worker scheduler

log "Backend rebuild complete"
