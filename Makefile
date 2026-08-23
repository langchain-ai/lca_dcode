.PHONY: install dev test lint fmt seed reset check

install:          ## Create the venv and install everything
	uv sync --extra dev

dev:              ## Run the app at http://127.0.0.1:8000
	uv run uvicorn ledger.main:app --reload

test:             ## Run the test suite
	uv run pytest

lint:             ## Check formatting and lint rules
	uv run ruff check .
	uv run ruff format --check .

fmt:              ## Fix formatting and autofixable lint errors
	uv run ruff format .
	uv run ruff check --fix .

seed:             ## Create ledger.db and fill it with sample data
	uv run python scripts/seed.py

reset:            ## Delete the database and reseed from scratch
	rm -f ledger.db
	$(MAKE) seed

check: lint test  ## What "done" means before you hand work back
