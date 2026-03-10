# Operations Runbook

## Daily operations

### Start / stop

```bash
./infra/scripts/up.sh
./infra/scripts/down.sh
```

### Tail logs

```bash
./infra/scripts/logs.sh
./infra/scripts/logs.sh nginx
./infra/scripts/logs.sh backend worker
```

## Log rotation

1. Docker container logs (stdout/stderr): configure Docker daemon log limits, for example in `/etc/docker/daemon.json`:
   ```json
   {
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "50m",
       "max-file": "5"
     }
   }
   ```
2. Restart Docker daemon after change:
   ```bash
   sudo systemctl restart docker
   ```
3. nginx file logs (`nginx_logs` volume): rotate by copying + truncating within container, or prefer stdout-only if your SIEM handles container logs.

## Rebuild a single service

Example: rebuild backend only.

```bash
docker compose -f compose.yaml -f compose.production.yaml build backend
docker compose -f compose.yaml -f compose.production.yaml up -d backend
```

## Roll out backend-only changes

```bash
docker compose -f compose.yaml -f compose.production.yaml build backend
docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
docker compose -f compose.yaml -f compose.production.yaml up -d backend worker scheduler
```

## Roll out frontend-only changes

```bash
docker compose -f compose.yaml -f compose.production.yaml build frontend
docker compose -f compose.yaml -f compose.production.yaml up -d frontend nginx
```

## Inspect healthchecks

```bash
docker compose -f compose.yaml -f compose.production.yaml ps
docker inspect --format '{{json .State.Health}}' $(docker compose -f compose.yaml -f compose.production.yaml ps -q db) | jq
docker inspect --format '{{json .State.Health}}' $(docker compose -f compose.yaml -f compose.production.yaml ps -q redis) | jq
docker inspect --format '{{json .State.Health}}' $(docker compose -f compose.yaml -f compose.production.yaml ps -q backend) | jq
docker inspect --format '{{json .State.Health}}' $(docker compose -f compose.yaml -f compose.production.yaml ps -q frontend) | jq
```

## Confirm service-to-service connectivity

### backend -> db

```bash
docker compose -f compose.yaml -f compose.production.yaml exec backend python -c "from app.db.session import wait_for_database; wait_for_database(); print('db ok')"
```

### backend -> redis

```bash
docker compose -f compose.yaml -f compose.production.yaml exec backend python -c "import redis, os; r=redis.Redis.from_url(os.environ['REDIS_URL']); print(r.ping())"
```

### nginx -> backend/frontend

```bash
docker compose -f compose.yaml -f compose.production.yaml exec nginx wget -qO- http://backend:8000/api/v1/health
docker compose -f compose.yaml -f compose.production.yaml exec nginx wget -qO- http://frontend:3000/api/health
```

## Run migrations safely

1. Ensure backup exists (`./infra/scripts/backup-db.sh`).
2. Deploy images (`./infra/scripts/build.sh`).
3. Run migrations:
   ```bash
   docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
   ```
4. Verify API health and critical workflows.
5. If migration fails, restore from backup using `restore-db.sh` and redeploy previous image tag.

