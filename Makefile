.PHONY: help install backend-install frontend-install lint test build dev backend-dev frontend-dev replay-bruteforce generate-synth

help:
	@echo "Targets:"
	@echo "  make install            Install backend and frontend dependencies"
	@echo "  make dev                Run full stack with Docker Compose"
	@echo "  make backend-dev        Run FastAPI backend locally"
	@echo "  make frontend-dev       Run frontend locally"
	@echo "  make replay-bruteforce TOKEN=<token>  Replay synthetic brute-force scenario"
	@echo "  make generate-synth     Generate synthetic log file"

install: backend-install frontend-install

backend-install:
	cd backend && python -m pip install -r requirements.txt

frontend-install:
	cd frontend && npm install

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

test:
	cd backend && pytest -q

build:
	cd frontend && npm run build

dev:
	docker compose up --build

backend-dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend-dev:
	cd frontend && npm run dev

replay-bruteforce:
	python scripts/ingest_logs.py data/brute_force_scenario.json --token "$(TOKEN)"

generate-synth:
	python scripts/generate_synthetic_logs.py
