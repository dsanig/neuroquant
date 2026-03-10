from decimal import Decimal


def csp_capital_at_risk(strike: Decimal, multiplier: int, contracts: int) -> Decimal:
    return strike * Decimal(multiplier) * Decimal(contracts)


def covered_call_notional(current_price: Decimal, multiplier: int, contracts: int) -> Decimal:
    return current_price * Decimal(multiplier) * Decimal(contracts)


def realized_unrealized_pnl(realized: Decimal, mark: Decimal, avg_price: Decimal, quantity: int, multiplier: int = 100) -> tuple[Decimal, Decimal]:
    unrealized = (mark - avg_price) * Decimal(quantity) * Decimal(multiplier)
    return realized, unrealized


def premium_capture(sold_premium: Decimal, bought_premium: Decimal) -> Decimal:
    return sold_premium - bought_premium


def concentration_metric(exposures: dict[str, Decimal]) -> Decimal:
    total_abs = sum((abs(v) for v in exposures.values()), Decimal("0"))
    if total_abs == 0:
        return Decimal("0")
    return max((abs(v) / total_abs for v in exposures.values()), default=Decimal("0"))
