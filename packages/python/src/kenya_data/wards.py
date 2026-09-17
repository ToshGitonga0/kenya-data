"""Ward lookups."""
from __future__ import annotations

import builtins
import sqlite3

from .constituencies import Constituencies
from .exceptions import EntityNotFoundError
from .models import Ward


class Wards:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def list(self) -> builtins.list[Ward]:
        rows = self._conn.execute(
            "SELECT id, code, name, constituency_id, status FROM wards ORDER BY name"
        ).fetchall()
        return [Ward(**dict(r)) for r in rows]

    def get(self, name_or_code: str) -> Ward:
        row = self._conn.execute(
            "SELECT id, code, name, constituency_id, status FROM wards "
            "WHERE name = ? COLLATE NOCASE OR code = ? COLLATE NOCASE",
            (name_or_code, name_or_code),
        ).fetchone()
        if row is None:
            raise EntityNotFoundError("ward", name_or_code)
        return Ward(**dict(row))

    def in_constituency(self, constituency_name_or_code: str) -> builtins.list[Ward]:
        constituency = Constituencies(self._conn).get(constituency_name_or_code)
        rows = self._conn.execute(
            "SELECT id, code, name, constituency_id, status FROM wards "
            "WHERE constituency_id = ? ORDER BY name",
            (constituency.id,),
        ).fetchall()
        return [Ward(**dict(r)) for r in rows]

    def in_county(self, county_name_or_code: str) -> builtins.list[Ward]:
        rows = self._conn.execute(
            """SELECT wards.id, wards.code, wards.name, wards.constituency_id, wards.status
               FROM wards
               JOIN constituencies ON constituencies.id = wards.constituency_id
               JOIN counties ON counties.id = constituencies.county_id
               WHERE counties.name = ? COLLATE NOCASE OR counties.code = ? COLLATE NOCASE
               ORDER BY wards.name""",
            (county_name_or_code, county_name_or_code),
        ).fetchall()
        return [Ward(**dict(r)) for r in rows]
