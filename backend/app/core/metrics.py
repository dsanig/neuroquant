from __future__ import annotations

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
except Exception:  # noqa: BLE001
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"

    class _NoopMetric:
        def labels(self, **_kwargs):
            return self

        def inc(self, _value: float = 1.0):
            return None

        def observe(self, _value: float):
            return None

    def Counter(*_args, **_kwargs):  # type: ignore[misc]
        return _NoopMetric()

    def Histogram(*_args, **_kwargs):  # type: ignore[misc]
        return _NoopMetric()

    def generate_latest() -> bytes:
        return b""


REQUEST_COUNT = Counter(
    "neuroquant_http_requests_total",
    "Total HTTP requests handled by backend",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "neuroquant_http_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)

CELERY_TASK_COUNT = Counter(
    "neuroquant_celery_tasks_total",
    "Total Celery tasks observed",
    ["task_name", "state"],
)
CELERY_TASK_FAILURES = Counter(
    "neuroquant_celery_task_failures_total",
    "Total failed Celery tasks",
    ["task_name"],
)

IMPORT_BATCH_COUNT = Counter(
    "neuroquant_import_batches_total",
    "Total import batches processed",
    ["source_system", "status"],
)
IMPORT_ERROR_COUNT = Counter(
    "neuroquant_import_errors_total",
    "Total import errors captured",
    ["code"],
)


def metrics_response() -> tuple[bytes, str]:
    return generate_latest(), CONTENT_TYPE_LATEST
