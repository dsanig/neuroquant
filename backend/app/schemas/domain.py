from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class UserMeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: str
    full_name: str
    roles: list[str]


class StrategyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: str | None


class PositionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    strategy_id: str
    quantity: int
    avg_price: Decimal
    mark_price: Decimal | None
    realized_pnl: Decimal


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    strategy_id: str
    symbol: str
    side: str
    quantity: int
    price: Decimal
    premium: Decimal | None
    executed_at: datetime
    roll_group_id: str | None


class RollDetectionResult(BaseModel):
    roll_groups_found: int


class DashboardSummaryOut(BaseModel):
    as_of: datetime
    open_positions: int
    trades_today: int
    active_strategies: int


class RiskSummaryOut(BaseModel):
    as_of: datetime
    portfolio_delta: Decimal
    portfolio_gamma: Decimal
    portfolio_theta: Decimal
    portfolio_vega: Decimal
    concentration_top_underlying: str | None
    underlying_exposure: dict[str, Decimal]


class MarginSummaryOut(BaseModel):
    as_of: datetime
    notional_exposure: Decimal
    capital_at_risk: Decimal
    margin_used: Decimal
    broker_requirement: Decimal


class PerformanceSummaryOut(BaseModel):
    as_of_date: date
    nav: Decimal
    pnl_day: Decimal
    pnl_mtd: Decimal | None
    pnl_ytd: Decimal | None


class IncomeEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    strategy_id: str | None
    event_date: date
    amount: Decimal
    event_type: str


class ImportBatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    filename: str
    source_checksum: str
    status: str
    row_count: int
    imported_count: int
    error_count: int


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    event_type: str
    entity_type: str
    entity_id: str
    payload: dict
    created_at: datetime
