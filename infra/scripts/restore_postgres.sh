#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <backup.sql.gz>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)
BACKUP_FILE="$1"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

cd "$ROOT_DIR"
source .env

if [[ -f "$BACKUP_FILE.sha256" ]]; then
  echo "[restore] Verifying checksum"
  sha256sum -c "$BACKUP_FILE.sha256"
else
  echo "[restore] Warning: checksum file not found ($BACKUP_FILE.sha256)"
fi

echo "[restore] Restoring $BACKUP_FILE into $POSTGRES_DB"
gunzip -c "$BACKUP_FILE" | docker compose "${COMPOSE_ARGS[@]}" exec -T db \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"

echo "[restore] Running post-restore health checks"
"$ROOT_DIR/infra/scripts/check_health.sh"
