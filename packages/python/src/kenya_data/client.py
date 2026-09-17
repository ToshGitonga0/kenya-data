"""The top-level Kenya Data client."""
from __future__ import annotations

import sqlite3
from pathlib import Path

from .constituencies import Constituencies
from .counties import Counties
from .dataset import Dataset
from .db import connect
from .wards import Wards


class Kenya:
    """Entry point for the Kenya Data SDK.

    >>> kenya = Kenya()
    >>> kenya.counties.list()          # doctest: +SKIP
    >>> kenya.counties.get("Nakuru")   # doctest: +SKIP
    """

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._conn: sqlite3.Connection = connect(db_path)
        self.counties = Counties(self._conn)
        self.constituencies = Constituencies(self._conn)
        self.wards = Wards(self._conn)
        self.dataset = Dataset(self._conn)

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> Kenya:  # noqa: PYI034 (Self requires Python >=3.11)
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()
