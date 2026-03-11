# NeuroQuant Disaster Recovery Runbook

## 1. Failure scenarios covered

- Host replacement
- Database corruption
- Bad migration requiring point-in-time rollback to latest backup
- Failed deployment requiring code rollback

## 2. Backup workflow (daily + before upgrade)

```bash
cd /srv/neuroquant
./infra/scripts/backup_postgres.sh
sha256sum -c backups/postgres_*.sha256
```

## 3. Restore workflow (database)

```bash
cd /srv/neuroquant
./infra/scripts/restore_postgres.sh backups/<backup_file>.sql.gz
./infra/scripts/check_health.sh
```

## 4. Full host rebuild workflow

```bash
# on new Debian VM
sudo mkdir -p /srv/neuroquant
sudo chown -R "$USER":"$USER" /srv/neuroquant
git clone <REPO_URL> /srv/neuroquant
cd /srv/neuroquant

# restore env files from secret store / backup bundle
cp /secure-location/.env .
cp /secure-location/backend.env backend/.env
cp /secure-location/frontend.env.local frontend/.env.local
cp /secure-location/infra.env infra/.env
chmod 600 .env backend/.env frontend/.env.local infra/.env

# deploy and restore DB
./infra/scripts/deploy.sh
./infra/scripts/restore_postgres.sh backups/<backup_file>.sql.gz
./infra/scripts/check_health.sh
```

## 5. Service-level emergency operations

```bash
# restart failed service only
docker compose -f compose.yaml -f compose.production.yaml restart backend

# inspect logs
docker compose -f compose.yaml -f compose.production.yaml logs -f --tail=200 backend

# rebuild failed service only
docker compose -f compose.yaml -f compose.production.yaml build backend
docker compose -f compose.yaml -f compose.production.yaml up -d backend
```

## 6. Rollback during incident

```bash
cd /srv/neuroquant
git checkout <LAST_KNOWN_GOOD_TAG>
./infra/scripts/deploy.sh
./infra/scripts/restore_postgres.sh backups/<pre_incident_backup>.sql.gz
./infra/scripts/check_health.sh
```

## 7. Mandatory validation after recovery

```bash
# database connectivity
docker compose -f compose.yaml -f compose.production.yaml exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT NOW();'

# API health
curl -fsS http://127.0.0.1/api/v1/health
curl -fsS http://127.0.0.1/healthz

# frontend
curl -fsSI http://127.0.0.1/

# async runtime
docker compose -f compose.yaml -f compose.production.yaml exec -T worker pgrep -fa 'celery.*worker'
docker compose -f compose.yaml -f compose.production.yaml exec -T scheduler pgrep -fa 'celery.*beat'
```
