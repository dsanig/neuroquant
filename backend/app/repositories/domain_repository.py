from datetime import date, datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.entities import (
    AuditLog,
    FileImportBatch,
    GreeksSnapshot,
    IncomeEvent,
    MarginMetric,
    PerformanceSnapshot,
    Position,
    RiskMetric,
    Strategy,
    Trade,
)


class DomainRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_strategies(self) -> list[Strategy]:
        return list(self.db.scalars(select(Strategy).order_by(Strategy.name)).all())

    def list_positions(self) -> list[Position]:
        return list(self.db.scalars(select(Position).order_by(Position.created_at.desc())).all())

    def list_trades(self) -> list[Trade]:
        return list(self.db.scalars(select(Trade).order_by(Trade.executed_at.desc())).all())

    def list_income_events(self) -> list[IncomeEvent]:
        return list(self.db.scalars(select(IncomeEvent).order_by(IncomeEvent.event_date.desc())).all())

    def list_import_batches(self) -> list[FileImportBatch]:
        return list(self.db.scalars(select(FileImportBatch).order_by(FileImportBatch.created_at.desc())).all())

    def list_audit_logs(self) -> list[AuditLog]:
        return list(self.db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc())).all())

    def count_open_positions(self) -> int:
        return self.db.scalar(select(func.count(Position.id)).where(Position.quantity != 0)) or 0

    def count_trades_for_day(self, utc_day: date) -> int:
        return self.db.scalar(select(func.count(Trade.id)).where(func.date(Trade.executed_at) == utc_day)) or 0

    def count_active_strategies(self) -> int:
        return self.db.scalar(select(func.count(Strategy.id))) or 0

    def latest_margin_summary(self) -> list[MarginMetric]:
        return list(self.db.scalars(select(MarginMetric).order_by(MarginMetric.measured_at.desc()).limit(100)).all())

    def latest_risk_metrics(self) -> list[RiskMetric]:
        return list(self.db.scalars(select(RiskMetric).order_by(RiskMetric.measured_at.desc()).limit(200)).all())

    def latest_greeks(self) -> list[GreeksSnapshot]:
        return list(self.db.scalars(select(GreeksSnapshot).order_by(GreeksSnapshot.snapshot_at.desc()).limit(200)).all())

    def latest_performance(self) -> PerformanceSnapshot | None:
        return self.db.scalar(select(PerformanceSnapshot).order_by(PerformanceSnapshot.snapshot_date.desc()))

    def utc_now(self) -> datetime:
        return datetime.now(timezone.utc)
