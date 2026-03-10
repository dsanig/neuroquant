#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/opt/neuroquant/repo}"
REPO_URL="${REPO_URL:-}"
VM_USER="${VM_USER:-${SUDO_USER:-$USER}}"

log() {
  echo "[setup-vm] $*"
}

require_root() {
  if [[ "${EUID}" -ne 0 ]]; then
    echo "[setup-vm] This script must run as root (try: sudo $0)" >&2
    exit 1
  fi
}

install_docker_engine() {
  log "Installing Docker Engine + Compose plugin prerequisites"
  apt-get update -y
  apt-get install -y ca-certificates curl gnupg git make

  install -m 0755 -d /etc/apt/keyrings
  if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
    log "Adding Docker apt repository key"
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
  fi

  local codename
  codename="$(. /etc/os-release && echo "${VERSION_CODENAME}")"
  cat > /etc/apt/sources.list.d/docker.list <<DOCKER_LIST
deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian ${codename} stable
DOCKER_LIST

  apt-get update -y
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
}

prepare_repo_dir() {
  log "Ensuring repository root exists at ${REPO_DIR}"
  install -d -m 0755 "$(dirname "${REPO_DIR}")"

  if [[ -d "${REPO_DIR}/.git" ]]; then
    log "Repository already exists; fetching latest refs"
    git -C "${REPO_DIR}" fetch --all --prune
  else
    if [[ -z "${REPO_URL}" ]]; then
      echo "[setup-vm] REPO_URL must be provided when cloning for the first time." >&2
      echo "[setup-vm] Example: REPO_URL=git@github.com:org/neuroquant.git sudo $0" >&2
      exit 1
    fi
    log "Cloning repository from ${REPO_URL}"
    git clone "${REPO_URL}" "${REPO_DIR}"
  fi

  chown -R "${VM_USER}:${VM_USER}" "$(dirname "${REPO_DIR}")"
}

bootstrap_env_files() {
  log "Bootstrapping missing .env files from examples"
  local files=(
    ".env"
    "backend/.env"
    "frontend/.env.local"
    "infra/.env"
  )

  for file in "${files[@]}"; do
    local example="${file}.example"
    if [[ ! -f "${REPO_DIR}/${file}" && -f "${REPO_DIR}/${example}" ]]; then
      cp "${REPO_DIR}/${example}" "${REPO_DIR}/${file}"
      log "Created ${file} from ${example}"
    fi
  done
}

main() {
  require_root
  log "Starting Debian VM bootstrap"
  install_docker_engine

  if id -nG "${VM_USER}" | tr ' ' '\n' | grep -qx docker; then
    log "User ${VM_USER} is already in docker group"
  else
    log "Adding ${VM_USER} to docker group"
    usermod -aG docker "${VM_USER}"
  fi

  prepare_repo_dir
  bootstrap_env_files

  log "Setup complete"
  log "Next: cd ${REPO_DIR} && make deploy"
}

main "$@"
