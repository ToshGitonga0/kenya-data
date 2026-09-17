"""Constituency lookups."""
from __future__ import annotations

import builtins
import sqlite3

from .counties import Counties
from .exceptions import EntityNotFoundError
from .models import Constituency


class Constituencies:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def list(self) -> builtins.list[Constituency]:
        rows = self._conn.execute(
            "SELECT id, code, name, county_id, status FROM constituencies ORDER BY name"
        ).fetchall()
        return [Constituency(**dict(r)) for r in rows]

    def get(self, name_or_code: str) -> Constituency:
        row = self._conn.execute(
            "SELECT id, code, name, county_id, status FROM constituencies "
            "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
            (name_or_code, name_or_code),
        ).fetchone()
        if row is None:
            raise EntityNotFoundError("constituency", name_or_code)
        return Constituency(**dict(row))

    def in_county(self, county_name_or_code: str) -> builtins.list[Constituency]:
        county = Counties(self._conn).get(county_name_or_code)
        rows = self._conn.execute(
            "SELECT id, code, name, county_id, status FROM constituencies "
            "WHERE county_id = ? ORDER BY name",
            (county.id,),
        ).fetchall()
        return [Constituency(**dict(r)) for r in rows]
