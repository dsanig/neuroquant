#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="$ROOT_DIR/backups"
mkdir -p "$BACKUP_DIR"

source "$ROOT_DIR/.env"

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="$BACKUP_DIR/postgres_${POSTGRES_DB}_${STAMP}.sql.gz"

cd "$ROOT_DIR"

docker compose -f compose.yaml -f compose.production.yaml exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=plain --no-owner --no-privileges \
  | gzip > "$OUT_FILE"

sha256sum "$OUT_FILE" > "$OUT_FILE.sha256"
echo "Backup created: $OUT_FILE"
