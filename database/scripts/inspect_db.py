#!/usr/bin/env python3
"""Print a quick structural summary of data/kenya.db."""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "data" / "kenya.db"


def main() -> int:
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    if not db_path.exists():
        print(f"No database at {db_path}. Run 'make build-db' first.", file=sys.stderr)
        return 1

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT version, status FROM dataset_versions ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        print(f"Dataset version: {row[0]} ({row[1]})")

    tables = [
        "counties", "sub_counties", "constituencies", "wards",
        "locations", "sub_locations", "coordinates", "boundaries",
        "population_statistics", "area_statistics", "data_sources",
    ]
    print("\nRow counts:")
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            print(f"  {t:<24} {cur.fetchone()[0]}")
        except sqlite3.OperationalError:
            print(f"  {t:<24} (table not found)")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
