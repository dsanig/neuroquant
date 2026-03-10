# Investment Control Center Upgrade Workflow

## 1. Pre-upgrade snapshot and backup

```bash
cd /srv/investment-control-center
git fetch --all --tags
./infra/scripts/backup_postgres.sh
cp .env .env.pre_upgrade.$(date +%Y%m%d_%H%M%S)
cp backend/.env backend/.env.pre_upgrade.$(date +%Y%m%d_%H%M%S)
cp frontend/.env.local frontend/.env.local.pre_upgrade.$(date +%Y%m%d_%H%M%S)
```

## 2. Pull target version

```bash
git checkout <TARGET_TAG_OR_BRANCH>
git pull --ff-only
```

## 3. Apply backend-only changes

```bash
./infra/scripts/redeploy_backend.sh
./infra/scripts/check_health.sh
```

Raw commands:

```bash
docker compose -f compose.yaml -f compose.production.yaml build backend
docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
docker compose -f compose.yaml -f compose.production.yaml up -d backend worker scheduler
```

## 4. Apply frontend-only changes

```bash
./infra/scripts/redeploy_frontend.sh
./infra/scripts/check_health.sh
```

Raw commands:

```bash
docker compose -f compose.yaml -f compose.production.yaml build frontend
docker compose -f compose.yaml -f compose.production.yaml up -d frontend nginx
```

## 5. Full stack upgrade

```bash
./infra/scripts/deploy.sh
./infra/scripts/check_health.sh
```

## 6. Rollback workflow

1. Identify last known-good Git tag/commit.
2. Restore code and redeploy containers.
3. If migration introduced incompatible schema/data, restore Postgres backup.

Commands:

```bash
# rollback code
git checkout <LAST_KNOWN_GOOD_TAG>

# redeploy images for old revision
./infra/scripts/deploy.sh

# optional: rollback database to captured backup
./infra/scripts/restore_postgres.sh backups/<backup_file>.sql.gz

# verify
./infra/scripts/check_health.sh
```

## 7. Post-upgrade validation checklist

```bash
# container health
docker compose -f compose.yaml -f compose.production.yaml ps

# API + DB dependency health
curl -fsS http://127.0.0.1/api/v1/health

# frontend reachability
curl -fsSI http://127.0.0.1/

# worker + scheduler logs
docker compose -f compose.yaml -f compose.production.yaml logs --tail=100 worker
docker compose -f compose.yaml -f compose.production.yaml logs --tail=100 scheduler
```
