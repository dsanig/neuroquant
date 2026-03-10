# Hardening Checklist

## Infrastructure
- [ ] Expose only nginx externally in production.
- [ ] Keep db/redis/backend/frontend on private Docker networks.
- [ ] Run app containers as non-root where practical.
- [ ] Add/verify healthchecks for all long-running services.
- [ ] Apply nginx security headers and request rate limits.
- [ ] Restrict inbound access to Cloudflare Tunnel, VPN, or private network.

## Application security
- [ ] Enforce JWT issuer/audience/expiry validation.
- [ ] Use HttpOnly + Secure + SameSite cookies for session token transport.
- [ ] Enforce RBAC for privileged routes.
- [ ] Enforce startup environment validation (fail closed in prod).
- [ ] Implement password policy and slow hash configuration.
- [ ] Ensure no development shortcuts (default secrets, debug configs) remain in production.

## Auditability
- [ ] Log successful and failed logins.
- [ ] Log import initiation and parsing outcomes.
- [ ] Log settings changes.
- [ ] Log privileged actions.
- [ ] Protect audit log read access by role.

## Backups and operations
- [ ] Encrypt backup artifacts and limit access.
- [ ] Perform periodic restore testing.
- [ ] Maintain patch/update cadence for base images and dependencies.
- [ ] Rotate secrets on schedule and after incidents.

## Production readiness checklist (concise)
- [ ] TLS enabled end-to-end (or trusted internal TLS termination boundary).
- [ ] Automated backups configured and monitored.
- [ ] Restore test completed and documented.
- [ ] Secret rotation policy implemented.
- [ ] Patch/update cadence documented and active.
- [ ] Least-privilege access model enforced.
- [ ] Monitoring coverage (app, infra, db) in place.
- [ ] Alerting configured for auth failures, errors, and service health.
- [ ] Log review workflow defined and operating.
