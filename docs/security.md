# Security Hardening Guide

## Deployment model
- Production deployment should expose **only nginx** externally.
- Backend, frontend, PostgreSQL, and Redis remain private on Docker internal networks.
- Access should be gated by Cloudflare Tunnel, VPN, or private network ingress controls.

## Auth/session/JWT hardening decisions
- Authentication uses short-lived JWT access tokens.
- JWTs include `iss`, `aud`, `iat`, `nbf`, `exp`, and `jti` claims and are validated server-side.
- Frontend stores auth token as an **HttpOnly**, `SameSite=Strict`, `Secure` (prod) cookie via Next.js route handler.
- CSRF strategy: because cookies are HttpOnly + SameSite Strict and APIs are same-origin behind internal ingress, risk is reduced; add CSRF token middleware before enabling cross-site form/API usage.
- Login endpoint is rate-limited at backend and nginx layers.

## RBAC and privileged operations
- RBAC checks are enforced server-side via `require_roles(...)` dependencies.
- Admin/operator roles are required for import ingestion/parsing and roll detection actions.
- Admin/auditor roles are required for audit log access.

## Audit logging
Audit events are persisted in `audit_logs` for:
- Successful login (`auth.login.success`)
- Failed login (`auth.login.failed`)
- Data import events (`data.import.uploaded`, parse queued/completed/failure events)
- Settings changes (`settings.changed`)
- Privileged actions (`trades.roll_detection.executed`)

## Secrets handling
- Never commit secrets to source control.
- Use an external secrets manager (Vault, cloud secret manager, SOPS, or Docker Swarm/Kubernetes secrets).
- Rotate JWT secrets, database credentials, and Grafana admin credentials on a fixed schedule.
- Production startup fails if `jwt_secret_key` is weak/default.

## Production/dev separation
- `ENVIRONMENT=production` is mandatory in production compose overlay.
- Production disallows SQLite and weak JWT secrets.
- Keep separate `.env` files and CI/CD secret scopes for dev vs prod.

## Backup/restore security notes
- Encrypt backups at rest and in transit.
- Restrict restore permissions to privileged operators.
- Keep restore logs and run scheduled restore drills in a non-production environment.
- Validate backup integrity and retention against compliance requirements.
