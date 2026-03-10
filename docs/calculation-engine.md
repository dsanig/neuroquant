# Calculation Engine Assumptions

All formulas are deterministic, stateless, and unit-tested.

## Margin and risk primitives
- **Cash-secured put capital at risk**: `strike * multiplier * contracts`
- **Covered call notional**: `current_price * multiplier * contracts`
- **Unrealized P&L**: `(mark - avg_price) * quantity * multiplier`
- **Premium capture**: `sold_premium - bought_premium`
- **Concentration metric**: `max(abs(exposure_i))/sum(abs(exposure_i))`

## Roll detection
A roll is detected if both trades exist in the same bucket with:
1. exact timestamp equality
2. same underlying
3. equal absolute quantity
4. one BUY and one SELL

Strike/expiration can differ because matching is based on underlying and quantity, enabling same-timestamp roll linkage between contracts.

## Portfolio summary rules
- Keep both broker-originated and app-calculated rows with `source` attribution.
- Portfolio aggregates are sums across latest rows (or configured lookback windows).
- Strategy and underlying breakdowns are additive and non-destructive.
