from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import AuditMixin


class MetricSource(StrEnum):
    BROKER = "broker"
    APP = "app"


class User(AuditMixin, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)


class Role(AuditMixin, Base):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(100), unique=True)


class UserRole(AuditMixin, Base):
    __tablename__ = "user_roles"
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), index=True)


class Instrument(AuditMixin, Base):
    __tablename__ = "instruments"
    symbol: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    underlying: Mapped[str] = mapped_column(String(24), index=True)
    instrument_type: Mapped[str] = mapped_column(String(32), index=True)


class Firm(AuditMixin, Base):
    __tablename__ = "firms"
    name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    legal_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    base_currency: Mapped[str] = mapped_column(String(3), default="USD")
    is_active: Mapped[bool] = mapped_column(default=True)


class BrokerAccount(AuditMixin, Base):
    __tablename__ = "broker_accounts"
    firm_id: Mapped[str] = mapped_column(ForeignKey("firms.id"), index=True)
    account_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    broker_name: Mapped[str] = mapped_column(String(100), index=True)


class Strategy(AuditMixin, Base):
    __tablename__ = "strategies"
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(Text)


class OptionContract(AuditMixin, Base):
    __tablename__ = "option_contracts"
    instrument_id: Mapped[str | None] = mapped_column(ForeignKey("instruments.id"), index=True)
    underlying: Mapped[str] = mapped_column(String(16), index=True)
    expiry: Mapped[date] = mapped_column(Date, index=True)
    strike: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    option_type: Mapped[str] = mapped_column(String(4))
    multiplier: Mapped[int] = mapped_column(Integer, default=100)


class Position(AuditMixin, Base):
    __tablename__ = "positions"
    strategy_id: Mapped[str] = mapped_column(ForeignKey("strategies.id"), index=True)
    broker_account_id: Mapped[str] = mapped_column(ForeignKey("broker_accounts.id"), index=True)
    option_contract_id: Mapped[str] = mapped_column(ForeignKey("option_contracts.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    avg_price: Mapped[Decimal] = mapped_column(Numeric(16, 6))
    mark_price: Mapped[Decimal | None] = mapped_column(Numeric(16, 6), nullable=True)
    realized_pnl: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=Decimal("0"))


class Trade(AuditMixin, Base):
    __tablename__ = "trades"
    __table_args__ = (UniqueConstraint("broker_account_id", "external_trade_id", name="uq_trade_external"),)
    broker_account_id: Mapped[str] = mapped_column(ForeignKey("broker_accounts.id"), index=True)
    strategy_id: Mapped[str] = mapped_column(ForeignKey("strategies.id"), index=True)
    option_contract_id: Mapped[str | None] = mapped_column(ForeignKey("option_contracts.id"), index=True)
    external_trade_id: Mapped[str] = mapped_column(String(128))
    symbol: Mapped[str] = mapped_column(String(24), index=True)
    side: Mapped[str] = mapped_column(String(8), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[Decimal] = mapped_column(Numeric(16, 6))
    premium: Mapped[Decimal | None] = mapped_column(Numeric(16, 6), nullable=True)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    roll_group_id: Mapped[str | None] = mapped_column(String(64), index=True)


class GreeksSnapshot(AuditMixin, Base):
    __tablename__ = "greeks_snapshots"
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    instrument_id: Mapped[str | None] = mapped_column(ForeignKey("instruments.id"), index=True)
    delta: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    gamma: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    theta: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    vega: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), nullable=True)
    source: Mapped[str] = mapped_column(String(32), default=MetricSource.APP.value)


class RiskMetric(AuditMixin, Base):
    __tablename__ = "risk_metrics"
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    instrument_id: Mapped[str | None] = mapped_column(ForeignKey("instruments.id"), index=True)
    metric_name: Mapped[str] = mapped_column(String(64), index=True)
    metric_value: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    source: Mapped[str] = mapped_column(String(32), default=MetricSource.APP.value)


class MarginMetric(AuditMixin, Base):
    __tablename__ = "margin_metrics"
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    notional_exposure: Mapped[Decimal] = mapped_column(Numeric(20, 4))
    capital_at_risk: Mapped[Decimal] = mapped_column(Numeric(20, 4), default=Decimal("0"))
    margin_used: Mapped[Decimal] = mapped_column(Numeric(20, 4))
    broker_requirement: Mapped[Decimal | None] = mapped_column(Numeric(20, 4))
    source: Mapped[str] = mapped_column(String(32), default=MetricSource.APP.value)


class PerformanceSnapshot(AuditMixin, Base):
    __tablename__ = "performance_snapshots"
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    nav: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    pnl_day: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    pnl_mtd: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    pnl_ytd: Mapped[Decimal | None] = mapped_column(Numeric(18, 4), nullable=True)
    source: Mapped[str] = mapped_column(String(32), default=MetricSource.APP.value)


class IncomeEvent(AuditMixin, Base):
    __tablename__ = "income_events"
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    event_date: Mapped[date] = mapped_column(Date, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 4))
    event_type: Mapped[str] = mapped_column(String(32), index=True)


class AuditLog(AuditMixin, Base):
    __tablename__ = "audit_logs"
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    entity_type: Mapped[str] = mapped_column(String(100), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict] = mapped_column(JSON)


class FileImportBatch(AuditMixin, Base):
    __tablename__ = "file_import_batches"
    __table_args__ = (UniqueConstraint("source_checksum", name="uq_file_import_checksum"),)
    filename: Mapped[str] = mapped_column(String(255), index=True)
    source_checksum: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    imported_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)


class FileImportRow(AuditMixin, Base):
    __tablename__ = "file_import_rows"
    import_batch_id: Mapped[str] = mapped_column(ForeignKey("file_import_batches.id"), index=True)
    row_number: Mapped[int] = mapped_column(Integer)
    raw_payload: Mapped[dict] = mapped_column(JSON)
    entity_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)


class ImportBatch(AuditMixin, Base):
    __tablename__ = "import_batch"
    intake_channel: Mapped[str] = mapped_column(String(32), index=True)
    source_system_name: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True, default="received")
    parser_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    parser_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    row_count: Mapped[int] = mapped_column(Integer, default=0)
    imported_count: Mapped[int] = mapped_column(Integer, default=0)
    error_count: Mapped[int] = mapped_column(Integer, default=0)


class ImportFile(AuditMixin, Base):
    __tablename__ = "import_file"
    import_batch_id: Mapped[str] = mapped_column(ForeignKey("import_batch.id"), index=True)
    original_filename: Mapped[str] = mapped_column(String(255), index=True)
    storage_uri: Mapped[str] = mapped_column(String(500))
    encrypted: Mapped[bool] = mapped_column(default=False)
    checksum_sha256: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    byte_size: Mapped[int] = mapped_column(Integer)
    mime_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    format_hint: Mapped[str | None] = mapped_column(String(64), nullable=True)
    detected_format: Mapped[str | None] = mapped_column(String(64), nullable=True)


class ImportError(AuditMixin, Base):
    __tablename__ = "import_error"
    import_batch_id: Mapped[str] = mapped_column(ForeignKey("import_batch.id"), index=True)
    import_file_id: Mapped[str | None] = mapped_column(ForeignKey("import_file.id"), nullable=True, index=True)
    severity: Mapped[str] = mapped_column(String(16), index=True, default="error")
    code: Mapped[str] = mapped_column(String(64), index=True)
    message: Mapped[str] = mapped_column(Text)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class ImportRowError(AuditMixin, Base):
    __tablename__ = "import_row_error"
    import_batch_id: Mapped[str] = mapped_column(ForeignKey("import_batch.id"), index=True)
    import_file_id: Mapped[str] = mapped_column(ForeignKey("import_file.id"), index=True)
    row_number: Mapped[int] = mapped_column(Integer, index=True)
    source_row: Mapped[dict] = mapped_column(JSON)
    code: Mapped[str] = mapped_column(String(64), index=True)
    message: Mapped[str] = mapped_column(Text)
    parser_version: Mapped[str] = mapped_column(String(32))


class SourceMappingMetadata(AuditMixin, Base):
    __tablename__ = "source_mapping_metadata"
    source_system_name: Mapped[str] = mapped_column(String(120), index=True)
    mapping_version: Mapped[str] = mapped_column(String(32), index=True)
    object_type: Mapped[str] = mapped_column(String(64), index=True)
    mapping_schema: Mapped[dict] = mapped_column(JSON)
    active: Mapped[bool] = mapped_column(default=True, index=True)


class TaskExecutionHistory(AuditMixin, Base):
    __tablename__ = "task_execution_history"
    task_name: Mapped[str] = mapped_column(String(255), index=True)
    celery_task_id: Mapped[str | None] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
