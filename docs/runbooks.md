# Operations Runbooks

## API not starting

1. `docker compose logs backend --tail=200`
2. Validate env: DB URL, JWT settings, Redis URL.
3. Check migrations + DB reachability from container.
4. Verify probe manually: `docker compose exec backend curl -fsS http://localhost:8000/healthz`

## Worker not consuming

1. `docker compose logs worker --tail=200`
2. Confirm queue flow: enqueue parse job and verify `task_id` appears.
3. Check Redis connectivity from worker container.
4. Confirm worker process: `docker compose exec worker pgrep -f 'celery.*worker'`

## Redis unavailable

1. `docker compose ps redis`
2. `docker compose logs redis --tail=200`
3. `docker compose exec redis redis-cli ping`
4. Verify backend dependency endpoint shows redis false: `/api/v1/health`.

## Postgres unavailable

1. `docker compose ps db`
2. `docker compose logs db --tail=200`
3. `docker compose exec db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"`
4. If failing, verify persistent volume integrity and credentials.

## Migration failed

1. `docker compose logs backend --tail=300`
2. Run manually: `docker compose exec backend alembic upgrade head`
3. Inspect `alembic_version` table.
4. Resolve incompatible schema/data state, re-run migration.

## Import stuck

1. Inspect batch status via API `/api/v1/imports/{id}`.
2. Search worker logs by `import_batch_id` and `task_id`.
3. Check metrics: `neuroquant_import_batches_total`, `neuroquant_import_errors_total`, `neuroquant_celery_task_failures_total`.
4. Re-queue parse task when root cause fixed.

## Frontend cannot reach backend

1. Validate backend readiness endpoint from frontend network namespace.
2. Check nginx upstream and frontend API base URL.
3. Validate CORS/proxy headers if requests fail in browser.
4. Inspect nginx access/error logs.

## Nginx routing broken

1. `docker compose logs nginx --tail=200`
2. Validate config: `docker compose exec nginx nginx -t`
3. Confirm upstream services healthy (`backend`, `frontend`).
4. Probe direct and via nginx to isolate hop failure.

## Rollback process

1. Identify last known-good image tags for backend/frontend.
2. Update deployment manifests or compose image refs.
3. Run DB rollback only if migration supports downgrade and data loss is acceptable.
4. Redeploy previous version.
5. Validate `/healthz`, `/readyz`, key API checks, and worker queue consumption.
6. Record incident timeline and corrective actions.
