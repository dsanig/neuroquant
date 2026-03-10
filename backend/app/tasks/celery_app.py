from celery import Celery

from app.core.config import settings

celery_app = Celery("icc", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.task_acks_late = True
celery_app.conf.task_default_retry_delay = 10
celery_app.conf.task_routes = {"app.tasks.jobs.*": {"queue": "default"}}
