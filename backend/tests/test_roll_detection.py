from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from app.services.roll_detection import RollDetectionService


def _trade(side: str, qty: int):
    return SimpleNamespace(
        id=str(uuid4()),
        option_contract_id="oc-1",
        symbol="AAPL",
        side=side,
        quantity=qty,
        executed_at=datetime(2026, 3, 10, 15, 30, tzinfo=UTC),
        roll_group_id=None,
    )


def test_roll_detected_with_exact_timestamp_underlying_and_quantity() -> None:
    buy = _trade("BUY", 2)
    sell = _trade("SELL", 2)
    contract = SimpleNamespace(id="oc-1", underlying="AAPL", expiry=datetime(2026, 6, 19).date(), strike=Decimal("100"))

    groups = RollDetectionService.assign_roll_groups([buy, sell], {"oc-1": contract})

    assert groups == 1
    assert buy.roll_group_id == sell.roll_group_id


def test_roll_not_detected_if_timestamp_differs() -> None:
    buy = _trade("BUY", 2)
    sell = _trade("SELL", 2)
    sell.executed_at = datetime(2026, 3, 10, 15, 30, 1, tzinfo=UTC)
    contract = SimpleNamespace(id="oc-1", underlying="AAPL")

    groups = RollDetectionService.assign_roll_groups([buy, sell], {"oc-1": contract})

    assert groups == 0
    assert buy.roll_group_id is None
    assert sell.roll_group_id is None
