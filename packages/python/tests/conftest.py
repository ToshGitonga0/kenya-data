"""Builds a throwaway SQLite database from the real approved data for each test session."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def test_db_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    db_path = tmp_path_factory.mktemp("kenya-data-db") / "kenya.db"
    seed_script = REPO_ROOT / "database" / "seeds" / "load_approved_data.py"
    subprocess.run([sys.executable, str(seed_script), str(db_path)], check=True)
    return db_path
