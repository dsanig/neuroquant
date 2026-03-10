#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_ARGS=(-f compose.yaml -f compose.production.yaml)
BACKUP_DIR="$ROOT_DIR/backups"

cd "$ROOT_DIR"
source .env

mkdir -p "$BACKUP_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_FILE="$BACKUP_DIR/postgres_${POSTGRES_DB}_${STAMP}.sql.gz"

echo "[backup] Creating $OUT_FILE"
docker compose "${COMPOSE_ARGS[@]}" exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" --format=plain --no-owner --no-privileges \
  | gzip > "$OUT_FILE"

sha256sum "$OUT_FILE" > "$OUT_FILE.sha256"
echo "[backup] SHA256: $(cat "$OUT_FILE.sha256")"
echo "[backup] Complete"
