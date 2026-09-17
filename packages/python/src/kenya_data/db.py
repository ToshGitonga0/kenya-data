"""Connection handling and default database resolution."""
from __future__ import annotations

import sqlite3
from pathlib import Path


def default_db_path() -> Path:
    """Resolve the bundled database shipped at the repo root.

    Layout assumed: packages/python/src/kenya_data/db.py -> ../../../../data/kenya.db
    """
    here = Path(__file__).resolve()
    repo_root = here.parents[4]
    return repo_root / "data" / "kenya.db"


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else default_db_path()
    if not path.exists():
        raise FileNotFoundError(
            f"No Kenya Data database found at {path}. "
            "Run 'make build-db' (or point Kenya(db_path=...) at an existing build)."
        )
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
