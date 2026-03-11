# NeuroQuant Deployment (Debian VM + Docker Compose)

## Operator automation quickstart

The repo includes an operator-grade automation layer for Debian VMs using Docker Engine and the Docker Compose plugin.

```bash
# 1) Bootstrap a fresh VM (installs Docker + clones repo to /opt/neuroquant/repo)
cd /opt/neuroquant/repo
sudo REPO_URL=<REPO_URL> make setup-vm

# 2) Configure environment files
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
cp infra/.env.example infra/.env

# 3) Full deployment (build + up + migrate + health)
make deploy

# 4) Fast daily loops
make rebuild-frontend      # rebuild/restart frontend + nginx only
make rebuild-backend       # rebuild/restart backend + worker + scheduler

# 5) Operations
make health
make logs                  # all services
REPO_DIR=/opt/neuroquant/repo ./infra/scripts/logs.sh backend worker
```

## Script reference

All scripts default to `REPO_DIR=/opt/neuroquant/repo`.

- `infra/scripts/setup-vm.sh`
  - Installs Docker Engine, Docker Compose plugin, git, and make.
  - Ensures the repo path exists and clones/fetches code.
  - Seeds missing `.env` files from `*.example` templates.
- `infra/scripts/deploy.sh`
  - Standard deploy flow: build images, start services, run migrations, run health checks.
  - Options: `--build-only`, `--skip-build`, `--skip-migrate`, `--skip-health`.
- `infra/scripts/rebuild-frontend.sh`
  - Rebuilds `frontend` and reconciles `frontend nginx`.
- `infra/scripts/rebuild-backend.sh`
  - Rebuilds `backend`, runs migrations (unless `--skip-migrate`), and reconciles `backend worker scheduler`.
- `infra/scripts/logs.sh [service ...]`
  - Streams compose logs for all services or selected services.
- `infra/scripts/health.sh`
  - Verifies compose status, DB connectivity, API/frontend reachability, and Celery worker/scheduler processes.

## Service names used by automation

The automation scripts use the compose service names defined in this repository:
`db`, `redis`, `backend`, `worker`, `scheduler`, `frontend`, `nginx`.
