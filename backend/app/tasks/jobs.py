from pathlib import Path

from celery.utils.log import get_task_logger

from app.db.session import SessionLocal
from app.models.entities import ImportFile
from app.services.imports import ImportService
from app.tasks.celery_app import celery_app

logger = get_task_logger(__name__)


@celery_app.task(bind=True, max_retries=5)
def recalculate_risk_metrics(self) -> str:
    try:
        logger.info("recalculate_risk_metrics.started")
        return "ok"
    except Exception as exc:  # noqa: BLE001
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3)
def parse_import_batch_async(self, import_batch_id: str) -> str:
    db = SessionLocal()
    try:
        logger.info("parse_import_batch_async.started", import_batch_id=import_batch_id)
        service = ImportService(db)
        import_file = db.query(ImportFile).filter(ImportFile.import_batch_id == import_batch_id).first()
        if not import_file:
            raise ValueError("import file not found")
        file_bytes = Path(import_file.storage_uri).read_bytes()
        service.parse_file(import_batch_id=import_batch_id, file_bytes=file_bytes)
        return "ok"
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        raise self.retry(exc=exc)
    finally:
        db.close()
