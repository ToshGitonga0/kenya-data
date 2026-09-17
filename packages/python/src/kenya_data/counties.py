"""County lookups."""
from __future__ import annotations

import builtins
import sqlite3

from .exceptions import EntityNotFoundError
from .models import County


class Counties:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def list(self) -> builtins.list[County]:
        rows = self._conn.execute(
            "SELECT id, code, name, capital, status FROM counties ORDER BY name"
        ).fetchall()
        return [County(**dict(r)) for r in rows]

    def get(self, name_or_code: str) -> County:
        row = self._conn.execute(
            "SELECT id, code, name, capital, status FROM counties "
            "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
            (name_or_code, name_or_code),
        ).fetchone()
        if row is None:
            raise EntityNotFoundError("county", name_or_code)
        return County(**dict(row))
