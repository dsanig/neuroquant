from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class NormalizedMetadata:
    import_batch_id: str
    source_file: str
    parser_version: str
    source_row: int | None = None


@dataclass(frozen=True)
class NormalizedTradeRecord:
    external_trade_id: str
    broker_account_number: str
    strategy_name: str
    symbol: str
    side: str
    quantity: int
    price: Decimal
    executed_at: datetime
    metadata: NormalizedMetadata
