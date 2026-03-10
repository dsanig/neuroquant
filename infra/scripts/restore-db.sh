#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <path-to-backup.sql.gz>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_FILE="$1"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

source "$ROOT_DIR/.env"

cd "$ROOT_DIR"

echo "Restoring $BACKUP_FILE into database $POSTGRES_DB"
echo "This operation overwrites data. Press Ctrl+C in the next 10 seconds to abort."
sleep 10

zcat "$BACKUP_FILE" | docker compose -f compose.yaml -f compose.production.yaml exec -T db \
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"

echo "Restore complete."
