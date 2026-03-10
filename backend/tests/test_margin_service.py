from app.services.margin_service import covered_call_notional, csp_capital_at_risk


def test_csp_capital_formula() -> None:
    assert csp_capital_at_risk(250, 100, 2) == 50000


def test_covered_call_notional() -> None:
    assert covered_call_notional(180, 100, 3) == 54000
