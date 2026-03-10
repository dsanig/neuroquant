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
    intake_channel: str
    source_system_name: str
    status: str
    parser_name: str | None
    parser_version: str | None
    row_count: int
    imported_count: int
    error_count: int


class ImportFileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    import_batch_id: str
    original_filename: str
    checksum_sha256: str
    byte_size: int
    encrypted: bool
    detected_format: str | None


class ImportErrorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    import_batch_id: str
    import_file_id: str | None
    severity: str
    code: str
    message: str


class ImportRowErrorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    import_batch_id: str
    import_file_id: str
    row_number: int
    source_row: dict
    code: str
    message: str
    parser_version: str


class ImportBatchDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    intake_channel: str
    source_system_name: str
    status: str
    parser_name: str | None
    parser_version: str | None
    row_count: int
    imported_count: int
    error_count: int
    files: list[ImportFileOut]
    errors: list[ImportErrorOut]
    row_errors: list[ImportRowErrorOut]


class ImportIntakeRequest(BaseModel):
    filename: str
    source_system_name: str
    intake_channel: str = "ui_upload"
    content_base64: str


class ImportParseRequest(BaseModel):
    content_base64: str


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    event_type: str
    entity_type: str
    entity_id: str
    payload: dict
    created_at: datetime
