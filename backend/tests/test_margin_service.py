from decimal import Decimal

from app.services.margin_service import (
    concentration_metric,
    covered_call_notional,
    csp_capital_at_risk,
    premium_capture,
    realized_unrealized_pnl,
)


def test_csp_capital_formula() -> None:
    assert csp_capital_at_risk(Decimal("250"), 100, 2) == Decimal("50000")


def test_covered_call_notional() -> None:
    assert covered_call_notional(Decimal("180"), 100, 3) == Decimal("54000")


def test_realized_unrealized_and_premium_capture() -> None:
    realized, unrealized = realized_unrealized_pnl(Decimal("10"), Decimal("2.2"), Decimal("2.0"), 5)
    assert realized == Decimal("10")
    assert unrealized == Decimal("100.0")
    assert premium_capture(Decimal("1500"), Decimal("1200")) == Decimal("300")


def test_concentration_metric() -> None:
    exposures = {"AAPL": Decimal("100"), "MSFT": Decimal("300")}
    assert concentration_metric(exposures) == Decimal("0.75")
