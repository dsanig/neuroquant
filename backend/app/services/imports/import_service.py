from __future__ import annotations

import csv
import hashlib
from io import StringIO
from pathlib import Path
from uuid import uuid4

import structlog
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.metrics import IMPORT_BATCH_COUNT, IMPORT_ERROR_COUNT
from app.models.entities import AuditLog, BrokerAccount, ImportBatch, ImportError, ImportFile, ImportRowError, Strategy, Trade
from app.services.imports.parsers.registry import ParserRegistry

logger = structlog.get_logger(__name__)


class ImportService:
    def __init__(self, db: Session, registry: ParserRegistry | None = None, actor_user_id: str | None = None):
        self.db = db
        self.registry = registry or ParserRegistry()
        self.actor_user_id = actor_user_id

    def upload_intake(self, *, filename: str, payload: bytes, source_system_name: str, intake_channel: str = "ui_upload") -> ImportBatch:
        checksum = hashlib.sha256(payload).hexdigest()
        existing_file = self.db.scalar(select(ImportFile).where(ImportFile.checksum_sha256 == checksum))
        if existing_file:
            logger.warning("import.upload.duplicate_checksum", filename=filename, checksum=checksum)
            raise ValueError("duplicate file checksum detected")

        batch = ImportBatch(intake_channel=intake_channel, source_system_name=source_system_name, status="received")
        self.db.add(batch)
        self.db.flush()

        storage_path = Path(settings.import_storage_dir) / str(batch.id)
        storage_path.mkdir(parents=True, exist_ok=True)
        file_path = storage_path / filename
        file_path.write_bytes(payload)

        import_file = ImportFile(
            import_batch_id=batch.id,
            original_filename=filename,
            storage_uri=str(file_path),
            checksum_sha256=checksum,
            byte_size=len(payload),
            format_hint=Path(filename).suffix.replace('.', '').lower() or None,
            encrypted=filename.endswith('.pgp') or filename.endswith('.gpg'),
            mime_type="text/csv" if filename.endswith(".csv") else None,
        )
        self.db.add(import_file)
        self._audit("data.import.uploaded", "import_batch", str(batch.id), {"file": filename, "checksum": checksum, "channel": intake_channel})
        logger.info("import.upload.accepted", import_batch_id=str(batch.id), filename=filename, source_system=source_system_name, intake_channel=intake_channel)
        self.db.commit()
        return batch

    def parse_file(self, *, import_batch_id: str, file_bytes: bytes) -> ImportBatch:
        batch = self.db.get(ImportBatch, import_batch_id)
        if not batch:
            raise ValueError("import batch not found")
        import_file = self.db.scalar(select(ImportFile).where(ImportFile.import_batch_id == import_batch_id))
        if not import_file:
            raise ValueError("import file not found")

        decoded = self._validate(file_bytes)
        headers, rows = self._detect_and_rows(decoded)
        parser = self.registry.detect(headers, batch.source_system_name)
        if not parser:
            self.capture_error(import_batch_id=batch.id, import_file_id=import_file.id, code="PARSER_NOT_FOUND", message="No parser matched file format")
            IMPORT_BATCH_COUNT.labels(source_system=batch.source_system_name, status="failed").inc()
            batch.status = "failed"
            logger.error("import.parse.parser_not_found", import_batch_id=str(batch.id), source_system=batch.source_system_name, headers=headers)
            self.db.commit()
            return batch

        batch.status = "processing"
        batch.parser_name = parser.parser_name
        batch.parser_version = parser.parser_version
        batch.row_count = len(rows)

        records, row_errors = parser.parse(rows=rows, import_batch_id=str(batch.id), source_file=import_file.original_filename)
        for row_number, code, message, source_row in row_errors:
            self.db.add(
                ImportRowError(
                    import_batch_id=batch.id,
                    import_file_id=import_file.id,
                    row_number=row_number,
                    source_row=source_row,
                    code=code,
                    message=message,
                    parser_version=parser.parser_version,
                )
            )
            IMPORT_ERROR_COUNT.labels(code=code).inc()

        imported = 0
        for record in records:
            broker_account = self._ensure_broker_account(record.broker_account_number, batch.source_system_name)
            strategy = self._ensure_strategy(record.strategy_name)
            existing_trade = self.db.scalar(
                select(Trade).where(
                    Trade.broker_account_id == broker_account.id,
                    Trade.external_trade_id == record.external_trade_id,
                )
            )
            if existing_trade:
                continue
            self.db.add(
                Trade(
                    broker_account_id=broker_account.id,
                    strategy_id=strategy.id,
                    option_contract_id=None,
                    external_trade_id=record.external_trade_id,
                    symbol=record.symbol,
                    side=record.side,
                    quantity=record.quantity,
                    price=record.price,
                    premium=None,
                    executed_at=record.executed_at,
                    roll_group_id=None,
                    source_file=record.metadata.source_file,
                    import_batch_id=str(record.metadata.import_batch_id),
                    source_system=batch.source_system_name,
                )
            )
            imported += 1

        batch.imported_count = imported
        batch.error_count = len(row_errors)
        batch.status = "completed" if not row_errors else "completed_with_errors"
        IMPORT_BATCH_COUNT.labels(source_system=batch.source_system_name, status=batch.status).inc()
        self._audit("data.import.parsed", "import_batch", str(batch.id), {"parser": parser.parser_name, "version": parser.parser_version, "rows": batch.row_count, "imported": imported, "errors": len(row_errors)})
        logger.info("import.parse.completed", import_batch_id=str(batch.id), parser=parser.parser_name, rows=batch.row_count, imported=imported, errors=len(row_errors), status=batch.status)
        self.db.commit()
        return batch

    def capture_error(self, *, import_batch_id: str, import_file_id: str | None, code: str, message: str, details: dict | None = None) -> None:
        IMPORT_ERROR_COUNT.labels(code=code).inc()
        logger.error("import.error.captured", import_batch_id=import_batch_id, import_file_id=import_file_id, code=code, message=message)
        self.db.add(
            ImportError(
                import_batch_id=import_batch_id,
                import_file_id=import_file_id,
                code=code,
                message=message,
                details=details,
                severity="error",
            )
        )

    def _validate(self, file_bytes: bytes) -> str:
        if not file_bytes:
            raise ValueError("file payload is empty")
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("file must be utf-8 encoded") from exc

    def _detect_and_rows(self, decoded: str) -> tuple[list[str], list[dict[str, str]]]:
        reader = csv.DictReader(StringIO(decoded))
        if not reader.fieldnames:
            raise ValueError("file header not detected")
        rows = [dict(row) for row in reader]
        return [h.strip() for h in reader.fieldnames], rows

    def _audit(self, event_type: str, entity_type: str, entity_id: str, payload: dict) -> None:
        self.db.add(AuditLog(actor_user_id=self.actor_user_id, event_type=event_type, entity_type=entity_type, entity_id=entity_id, payload=payload))

    def _ensure_broker_account(self, account_number: str, broker_name: str) -> BrokerAccount:
        account = self.db.scalar(select(BrokerAccount).where(BrokerAccount.account_number == account_number))
        if account:
            return account
        account = BrokerAccount(account_number=account_number, broker_name=broker_name)
        self.db.add(account)
        self.db.flush()
        return account

    def _ensure_strategy(self, strategy_name: str) -> Strategy:
        strategy = self.db.scalar(select(Strategy).where(Strategy.name == strategy_name))
        if strategy:
            return strategy
        strategy = Strategy(name=strategy_name, description=f"Auto-created from import {uuid4().hex[:8]}")
        self.db.add(strategy)
        self.db.flush()
        return strategy
