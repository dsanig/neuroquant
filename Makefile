COMPOSE=docker compose

.PHONY: up down logs build migrate seed test lint format

up:
	$(COMPOSE) -f compose.yaml up -d --build

down:
	$(COMPOSE) -f compose.yaml down

logs:
	$(COMPOSE) -f compose.yaml logs -f --tail=200

build:
	$(COMPOSE) -f compose.yaml build

migrate:
	$(COMPOSE) -f compose.yaml run --rm backend alembic upgrade head

seed:
	$(COMPOSE) -f compose.yaml run --rm backend python -m app.seed

test:
	$(COMPOSE) -f compose.yaml run --rm backend pytest -q

lint:
	$(COMPOSE) -f compose.yaml run --rm backend ruff check app
	$(COMPOSE) -f compose.yaml run --rm frontend npm run lint

format:
	$(COMPOSE) -f compose.yaml run --rm backend ruff format app
