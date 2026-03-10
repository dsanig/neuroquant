from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import AuditMixin


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


class BrokerAccount(AuditMixin, Base):
    __tablename__ = "broker_accounts"
    account_number: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    broker_name: Mapped[str] = mapped_column(String(100), index=True)


class Strategy(AuditMixin, Base):
    __tablename__ = "strategies"
    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[str | None] = mapped_column(Text)


class OptionContract(AuditMixin, Base):
    __tablename__ = "option_contracts"
    underlying: Mapped[str] = mapped_column(String(16), index=True)
    expiry: Mapped[date] = mapped_column(Date, index=True)
    strike: Mapped[float] = mapped_column(Float)
    option_type: Mapped[str] = mapped_column(String(4))
    multiplier: Mapped[int] = mapped_column(Integer, default=100)


class Position(AuditMixin, Base):
    __tablename__ = "positions"
    strategy_id: Mapped[str] = mapped_column(ForeignKey("strategies.id"), index=True)
    broker_account_id: Mapped[str] = mapped_column(ForeignKey("broker_accounts.id"), index=True)
    option_contract_id: Mapped[str] = mapped_column(ForeignKey("option_contracts.id"), index=True)
    quantity: Mapped[int] = mapped_column(Integer)
    avg_price: Mapped[float] = mapped_column(Float)


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
    price: Mapped[float] = mapped_column(Float)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    roll_group_id: Mapped[str | None] = mapped_column(String(64), index=True)


class DailySnapshot(AuditMixin, Base):
    __tablename__ = "daily_snapshots"
    snapshot_date: Mapped[date] = mapped_column(Date, index=True)
    nav: Mapped[float] = mapped_column(Numeric(18, 4))
    pnl_day: Mapped[float] = mapped_column(Numeric(18, 4))


class GreeksSnapshot(AuditMixin, Base):
    __tablename__ = "greeks_snapshots"
    snapshot_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    delta: Mapped[float] = mapped_column(Float)
    gamma: Mapped[float] = mapped_column(Float)
    theta: Mapped[float] = mapped_column(Float)
    vega: Mapped[float] = mapped_column(Float)


class IncomeEvent(AuditMixin, Base):
    __tablename__ = "income_events"
    event_date: Mapped[date] = mapped_column(Date, index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 4))
    event_type: Mapped[str] = mapped_column(String(32), index=True)


class RiskMetric(AuditMixin, Base):
    __tablename__ = "risk_metrics"
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    metric_name: Mapped[str] = mapped_column(String(64), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(20, 6))
    source: Mapped[str] = mapped_column(String(32), default="app")


class MarginMetric(AuditMixin, Base):
    __tablename__ = "margin_metrics"
    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    strategy_id: Mapped[str | None] = mapped_column(ForeignKey("strategies.id"), index=True)
    notional_exposure: Mapped[float] = mapped_column(Numeric(20, 4))
    margin_used: Mapped[float] = mapped_column(Numeric(20, 4))
    broker_requirement: Mapped[float | None] = mapped_column(Numeric(20, 4))
    source: Mapped[str] = mapped_column(String(32), default="app")


class AuditLog(AuditMixin, Base):
    __tablename__ = "audit_logs"
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    entity_type: Mapped[str] = mapped_column(String(100), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[str] = mapped_column(Text)


class FileImport(AuditMixin, Base):
    __tablename__ = "file_imports"
    filename: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    row_count: Mapped[int] = mapped_column(Integer, default=0)


class TaskExecutionHistory(AuditMixin, Base):
    __tablename__ = "task_execution_history"
    task_name: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
