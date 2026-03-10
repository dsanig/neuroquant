#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

if [[ $# -eq 0 ]]; then
  docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200
else
  docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200 "$@"
fi
