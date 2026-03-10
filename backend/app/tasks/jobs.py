from celery.utils.log import get_task_logger

from app.tasks.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=5)
def recalculate_risk_metrics(self) -> str:
    try:
        logger.info("recalculate_risk_metrics.started")
        return "ok"
    except Exception as exc:  # noqa: BLE001
        raise self.retry(exc=exc)
