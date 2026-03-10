import base64

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.entities import ImportBatch, ImportError, ImportFile, ImportRowError
from app.schemas.domain import (
    ImportBatchDetailOut,
    ImportBatchOut,
    ImportErrorOut,
    ImportFileOut,
    ImportIntakeRequest,
    ImportParseRequest,
    ImportRowErrorOut,
    UserMeOut,
)
from app.services.imports import ImportService
from app.tasks.jobs import parse_import_batch_async

router = APIRouter()


@router.get("", response_model=list[ImportBatchOut])
def list_imports(_: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ImportBatchOut]:
    batches = db.scalars(select(ImportBatch).order_by(ImportBatch.created_at.desc())).all()
    return [ImportBatchOut.model_validate(batch, from_attributes=True) for batch in batches]


@router.post("/intake", response_model=ImportBatchOut)
def intake_import(req: ImportIntakeRequest, _: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> ImportBatchOut:
    service = ImportService(db)
    try:
        payload = base64.b64decode(req.content_base64)
        batch = service.upload_intake(
            filename=req.filename,
            payload=payload,
            source_system_name=req.source_system_name,
            intake_channel=req.intake_channel,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ImportBatchOut.model_validate(batch, from_attributes=True)


@router.post("/{import_batch_id}/parse", response_model=dict)
def enqueue_parse(import_batch_id: str, _: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    batch = db.get(ImportBatch, import_batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Import batch not found")
    task = parse_import_batch_async.delay(import_batch_id)
    return {"task_id": task.id, "status": "queued"}


@router.post("/{import_batch_id}/parse-inline", response_model=ImportBatchOut)
def parse_inline(import_batch_id: str, req: ImportParseRequest, _: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> ImportBatchOut:
    service = ImportService(db)
    try:
        file_bytes = base64.b64decode(req.content_base64)
        batch = service.parse_file(import_batch_id=import_batch_id, file_bytes=file_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ImportBatchOut.model_validate(batch, from_attributes=True)


@router.get("/{import_batch_id}", response_model=ImportBatchDetailOut)
def get_import_batch(import_batch_id: str, _: UserMeOut = Depends(get_current_user), db: Session = Depends(get_db)) -> ImportBatchDetailOut:
    batch = db.get(ImportBatch, import_batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Import batch not found")
    files = db.scalars(select(ImportFile).where(ImportFile.import_batch_id == import_batch_id).order_by(ImportFile.created_at.desc())).all()
    errors = db.scalars(select(ImportError).where(ImportError.import_batch_id == import_batch_id).order_by(ImportError.created_at.desc())).all()
    row_errors = db.scalars(select(ImportRowError).where(ImportRowError.import_batch_id == import_batch_id).order_by(ImportRowError.row_number.asc())).all()
    return ImportBatchDetailOut(
        id=str(batch.id),
        intake_channel=batch.intake_channel,
        source_system_name=batch.source_system_name,
        status=batch.status,
        parser_name=batch.parser_name,
        parser_version=batch.parser_version,
        row_count=batch.row_count,
        imported_count=batch.imported_count,
        error_count=batch.error_count,
        files=[ImportFileOut.model_validate(f, from_attributes=True) for f in files],
        errors=[ImportErrorOut.model_validate(e, from_attributes=True) for e in errors],
        row_errors=[ImportRowErrorOut.model_validate(e, from_attributes=True) for e in row_errors],
    )
