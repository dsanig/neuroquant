REPO_DIR ?= /opt/neuroquant/repo

.PHONY: setup-vm deploy rebuild-frontend rebuild-backend logs health

setup-vm:
	sudo REPO_DIR="$(REPO_DIR)" ./infra/scripts/setup-vm.sh

deploy:
	REPO_DIR="$(REPO_DIR)" ./infra/scripts/deploy.sh

rebuild-frontend:
	REPO_DIR="$(REPO_DIR)" ./infra/scripts/rebuild-frontend.sh

rebuild-backend:
	REPO_DIR="$(REPO_DIR)" ./infra/scripts/rebuild-backend.sh

logs:
	REPO_DIR="$(REPO_DIR)" ./infra/scripts/logs.sh

health:
	REPO_DIR="$(REPO_DIR)" ./infra/scripts/health.sh
