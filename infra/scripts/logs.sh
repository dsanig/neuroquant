#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
COMPOSE_FILES=( -f compose.yaml -f compose.production.yaml )

cd "$REPO_DIR"

echo "[logs] Streaming logs (Ctrl+C to stop)"
if [[ $# -eq 0 ]]; then
  docker compose "${COMPOSE_FILES[@]}" logs -f --tail=200
else
  docker compose "${COMPOSE_FILES[@]}" logs -f --tail=200 "$@"
fi
