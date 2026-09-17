"""Dataset (as opposed to SDK) version metadata."""
from __future__ import annotations

import sqlite3

from .models import DatasetInfo


class Dataset:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def info(self) -> DatasetInfo:
        row = self._conn.execute(
            "SELECT version, status, created_at FROM dataset_versions "
            "ORDER BY id DESC LIMIT 1"
        ).fetchone()
        if row is None:
            return DatasetInfo(version="unknown", status="unknown", updated_at="unknown")
        return DatasetInfo(version=row["version"], status=row["status"], updated_at=row["created_at"])

    @property
    def version(self) -> str:
        return self.info().version

    @property
    def updated_at(self) -> str:
        return self.info().updated_at
