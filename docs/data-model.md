# Data Model Overview

## Identity and RBAC
- `users`
- `roles`
- `user_roles`

## Trading domain
- `firms` (single firm today, multi-firm ready)
- `strategies`
- `broker_accounts` (single account today, multi-account ready)
- `instruments`
- `option_contracts`
- `trades` (historical immutable ledger + roll linkage)
- `positions` (grouped by strategy)

## Metrics and analytics
- `greeks_snapshots` (delta/gamma/theta/vega + source)
- `risk_metrics` (name/value + source)
- `margin_metrics` (notional, capital at risk, margin used, broker requirement, source)
- `performance_snapshots` (daily and historical NAV/P&L)
- `income_events`

## Governance
- `audit_logs`
- `task_execution_history`

## Import pipeline
- `file_import_batches` (idempotency via source checksum)
- `file_import_rows` (traceability to source row + mapped entity + errors)

Every imported or generated object can be attributed using shared audit metadata in `AuditMixin`.
