# Investment Control Center Roadmap

## Phase 1 (current scaffold)
- [x] Monorepo and dockerized local/prod baseline
- [x] Core entities and migration baseline
- [x] Auth + RBAC foundations
- [x] Initial dashboard/navigation shell
- [x] Roll detection service logic baseline

## Phase 2 (ingestion and operations)
- [ ] Broker file adapters (IBKR, Tastytrade, Schwab)
- [ ] CSV/XLSX schema registry + validation DSL
- [ ] Deterministic import replay and reconciliation
- [ ] Operational runbooks and SLO dashboards

## Phase 3 (advanced risk and margin)
- [ ] Scenario stress engine (vol/rate/spot shocks)
- [ ] Intraday greeks and VaR backtesting
- [ ] Portfolio-level concentration/sector/geography limits
- [ ] Cross-strategy margin optimization suggestions

## Phase 4 (multi-account and multi-user)
- [ ] Multi-broker and account hierarchy
- [ ] Fine-grained row/strategy access policies
- [ ] SSO/SAML/OIDC integration
- [ ] Approval workflows and maker-checker controls

## Phase 5 (platform hardening)
- [ ] Blue/green deployment workflow
- [ ] Formal data retention and archive policy
- [ ] Immutable audit exports and legal hold tooling
- [ ] DR drills and backup restoration automation
