import structlog
from celery import Celery
from celery.signals import task_failure, task_postrun, task_prerun

from app.core.config import settings
from app.core.metrics import CELERY_TASK_COUNT, CELERY_TASK_FAILURES

celery_app = Celery("icc", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_acks_late = True
celery_app.conf.task_default_retry_delay = 10
celery_app.conf.task_routes = {"app.tasks.jobs.*": {"queue": "default"}}

logger = structlog.get_logger("celery")


@task_prerun.connect
def on_task_prerun(task_id=None, task=None, args=None, kwargs=None, **_kwargs):
    task_name = task.name if task else "unknown"
    structlog.contextvars.bind_contextvars(task_id=task_id, task_name=task_name)
    CELERY_TASK_COUNT.labels(task_name=task_name, state="started").inc()
    logger.info("celery.task.started", task_id=task_id, task_name=task_name, args=args, kwargs=kwargs)


@task_postrun.connect
def on_task_postrun(task_id=None, task=None, state=None, retval=None, **_kwargs):
    task_name = task.name if task else "unknown"
    CELERY_TASK_COUNT.labels(task_name=task_name, state=(state or "unknown").lower()).inc()
    logger.info("celery.task.completed", task_id=task_id, task_name=task_name, state=state, return_value=str(retval))
    structlog.contextvars.clear_contextvars()


@task_failure.connect
def on_task_failure(task_id=None, exception=None, traceback=None, sender=None, **_kwargs):
    task_name = sender.name if sender else "unknown"
    CELERY_TASK_FAILURES.labels(task_name=task_name).inc()
    logger.error("celery.task.failed", task_id=task_id, task_name=task_name, error=str(exception), traceback=str(traceback))
