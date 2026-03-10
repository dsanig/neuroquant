# Deployment Guide (Docker Compose)

This guide provides a reproducible, production-oriented deployment for the Investment Control Center on self-hosted Debian VMs.

## 1) Prerequisites

- Debian VM with Docker Engine 24+ and Docker Compose v2
- Access to this repository
- Firewall rules allowing inbound traffic only to nginx (`80` and optionally `443`)

## 2) Environment preparation

Create environment files from templates and fill values with secure secrets:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
cp infra/.env.example infra/.env
```

Security rules:

- Never commit `.env` files.
- Use long random values for JWT/admin credentials.
- Keep database credentials in sync between `.env` and `backend/.env` (`DATABASE_URL`).

## 3) Build and start

Production stack (only nginx exposed externally):

```bash
./infra/scripts/build.sh
./infra/scripts/up.sh
```

Equivalent raw command:

```bash
docker compose -f compose.yaml -f compose.production.yaml up -d --build
```

## 4) Database migrations (safe workflow)

Run migrations explicitly after images start:

```bash
docker compose -f compose.yaml -f compose.production.yaml run --rm backend alembic upgrade head
```

Recommended rollout order:

1. Deploy code (`build.sh`)
2. Run migrations
3. Restart backend and worker if needed

```bash
./infra/scripts/restart-service.sh backend
./infra/scripts/restart-service.sh worker
./infra/scripts/restart-service.sh scheduler
```

## 5) Health and verification

Check container status:

```bash
docker compose -f compose.yaml -f compose.production.yaml ps
```

Inspect healthcheck output:

```bash
docker inspect --format '{{json .State.Health}}' $(docker compose -f compose.yaml -f compose.production.yaml ps -q backend) | jq
```

Test ingress:

```bash
curl -fsS http://127.0.0.1/api/v1/health
curl -fsS http://127.0.0.1/api/health
```

## 6) Network model

- `app` network: nginx, frontend, backend
- `data` internal network: db, redis, backend, worker, scheduler
- In production override:
  - `db`, `redis`, `backend`, and `frontend` are **not** host-published
  - nginx is the only public entrypoint

## 7) Cloudflare Tunnel / internal reverse proxy notes

### Option A: Cloudflare Tunnel in front of nginx

- Keep nginx listening on `80` internally.
- Run cloudflared on host or sidecar and point tunnel to `http://nginx:80`.
- Restrict VM firewall to block direct public access if tunnel is the only ingress path.

### Option B: Corporate reverse proxy/VPN ingress

- Keep nginx private on internal VLAN.
- Terminate TLS at upstream proxy, forward `X-Forwarded-*` headers.
- Optionally enable direct TLS in nginx by mounting certs and adding `443` listener in `infra/nginx/nginx.conf`.

## 8) Logging strategy

- Primary logs: container stdout/stderr (`docker compose logs`)
- nginx additionally writes file logs under named volume `nginx_logs`
- Configure host-level log rotation for Docker daemon JSON logs and rotate/archive nginx volume logs periodically

