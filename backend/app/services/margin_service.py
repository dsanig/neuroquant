def csp_capital_at_risk(strike: float, multiplier: int, contracts: int) -> float:
    return strike * multiplier * contracts


def covered_call_notional(current_price: float, multiplier: int, contracts: int) -> float:
    return current_price * multiplier * contracts
