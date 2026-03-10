#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
COMPOSE_FILES=( -f compose.yaml -f compose.production.yaml )

log() {
  echo "[rebuild-frontend] $*"
}

cd "$REPO_DIR"

log "Building frontend image"
docker compose "${COMPOSE_FILES[@]}" build frontend

log "Restarting frontend and nginx"
docker compose "${COMPOSE_FILES[@]}" up -d frontend nginx

log "Frontend rebuild complete"
