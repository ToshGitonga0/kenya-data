.PHONY: setup test lint format validate build-db inspect-db

# All Python targets run inside a local .venv, created by `make setup`.
# This avoids "externally-managed-environment" errors on systems (e.g.
# Homebrew Python on macOS) that refuse `pip install` outside a venv.
PYTHON := $(shell [ -x $(CURDIR)/.venv/bin/python3 ] && echo $(CURDIR)/.venv/bin/python3 || echo python3)

setup:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e "packages/python[dev]"
	cd packages/typescript && npm install

test:
	cd packages/python && $(PYTHON) -m pytest
	cd packages/typescript && npm test

lint:
	cd packages/python && $(PYTHON) -m ruff check src tests
	cd packages/python && $(PYTHON) -m mypy src
	cd packages/typescript && npm run lint

format:
	cd packages/python && $(PYTHON) -m ruff format src tests
	cd packages/typescript && npm run format

validate:
	$(PYTHON) scripts/validate-data/validate.py

build-db:
	$(PYTHON) database/seeds/load_approved_data.py data/kenya.db

inspect-db:
	$(PYTHON) database/scripts/inspect_db.py
