# Monitoring Guide

This service now exposes a baseline observability surface for operators.

## Signals available

- **Structured logs (JSON)** for API and Celery worker flows.
- **Correlation IDs** (`x-request-id`) on every API response and request log.
- **Celery task IDs** in worker logs via `task_id` context binding.
- **Health probes**:
  - `GET /healthz` (liveness)
  - `GET /readyz` (readiness; checks DB)
  - `GET /api/v1/health` (dependency status for Postgres + Redis)
- **Metrics**:
  - `neuroquant_http_requests_total`
  - `neuroquant_http_request_latency_seconds`
  - `neuroquant_celery_tasks_total`
  - `neuroquant_celery_task_failures_total`
  - `neuroquant_import_batches_total`
  - `neuroquant_import_errors_total`

## Monitoring profile (Compose)

Enable optional Prometheus + Grafana with:

```bash
docker compose -f compose.yaml -f compose.production.yaml --profile monitoring up -d
```

### Endpoints

- Prometheus: `http://localhost:${PROMETHEUS_PORT:-9090}`
- Grafana: `http://localhost:${GRAFANA_PORT:-3001}`
- Backend metrics target: `http://backend:8000/metrics`

## Probe strategy

- **Liveness (`/healthz`)**: should only tell if process is running.
- **Readiness (`/readyz`)**: should fail when DB connectivity fails, removing instance from service.
- **Dependency endpoint (`/api/v1/health`)**: for operator diagnostics (degraded if Redis or Postgres unavailable).

## Practical triage flow

1. Check liveness: `curl -fsS http://localhost:8000/healthz`
2. Check readiness: `curl -fsS http://localhost:8000/readyz`
3. Check dependency matrix: `curl -fsS http://localhost:8000/api/v1/health`
4. Inspect recent logs for shared `request_id` / `task_id`.
5. Check Prometheus counters for spikes in `neuroquant_import_errors_total` and `neuroquant_celery_task_failures_total`.
