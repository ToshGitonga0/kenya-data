"""Connection handling and packaged database resolution."""

from __future__ import annotations

import sqlite3
from importlib.resources import files
from pathlib import Path


def default_db_path() -> Path:
    packaged = Path(str(files("kenya_data").joinpath("kenya.db")))
    if packaged.exists():
        return packaged

    # Local repository fallback.
    return Path(__file__).resolve().parents[4] / "data" / "kenya.db"


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else default_db_path()

    if not path.exists():
        raise FileNotFoundError(f"No Kenya Data database found at {path}")

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
