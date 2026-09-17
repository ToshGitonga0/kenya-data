#!/usr/bin/env python3
"""
Kenya Data validation framework.

Runs structural, referential, geographic, statistical, and source
checks against a built SQLite database. Exits non-zero if any check
fails. See docs/data-quality.md for what each category covers.

Usage:
    python3 scripts/validate-data/validate.py [path/to/kenya.db]
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = REPO_ROOT / "data" / "kenya.db"

ADMIN_TABLES = ["counties", "sub_counties", "constituencies", "wards", "locations", "sub_locations"]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def ok(self) -> bool:
        return not self.errors


def check_structural(conn: sqlite3.Connection, report: Report) -> None:
    """Required fields, nullability, unique identifiers, duplicates."""
    for table in ADMIN_TABLES:
        rows = conn.execute(f"SELECT id, code, name FROM {table}").fetchall()
        seen_codes: set[str] = set()
        for row in rows:
            if not row["code"]:
                report.error(f"{table}.id={row['id']}: missing code")
            if not row["name"]:
                report.error(f"{table}.id={row['id']}: missing name")
            if row["code"] in seen_codes:
                report.error(f"{table}: duplicate code {row['code']!r}")
            seen_codes.add(row["code"])


def check_referential(conn: sqlite3.Connection, report: Report) -> None:
    """Every child references a parent that actually exists."""
    edges = [
        ("sub_counties", "county_id", "counties"),
        ("constituencies", "county_id", "counties"),
        ("wards", "constituency_id", "constituencies"),
        ("locations", "ward_id", "wards"),
        ("sub_locations", "location_id", "locations"),
    ]
    for child, fk, parent in edges:
        orphans = conn.execute(
            f"""SELECT {child}.id FROM {child}
                LEFT JOIN {parent} ON {parent}.id = {child}.{fk}
                WHERE {parent}.id IS NULL"""
        ).fetchall()
        for row in orphans:
            report.error(f"{child}.id={row['id']}: {fk} does not reference an existing {parent} row")


def check_geographic(conn: sqlite3.Connection, report: Report) -> None:
    """Coordinate ranges and suspicious duplicates."""
    rows = conn.execute("SELECT id, latitude, longitude, entity_type, entity_id FROM coordinates").fetchall()
    seen: dict[tuple[float, float], list[int]] = {}
    for row in rows:
        if not (-90 <= row["latitude"] <= 90):
            report.error(f"coordinates.id={row['id']}: latitude out of range")
        if not (-180 <= row["longitude"] <= 180):
            report.error(f"coordinates.id={row['id']}: longitude out of range")
        key = (row["latitude"], row["longitude"])
        seen.setdefault(key, []).append(row["id"])
    for key, ids in seen.items():
        if len(ids) > 1:
            report.warn(f"coordinates: {len(ids)} entities share the exact point {key} (ids={ids})")


def check_statistical(conn: sqlite3.Connection, report: Report) -> None:
    """Population/area sanity checks."""
    for row in conn.execute("SELECT id, population, reference_year FROM population_statistics"):
        if row["population"] < 0:
            report.error(f"population_statistics.id={row['id']}: negative population")
        if row["reference_year"] and (row["reference_year"] < 1900 or row["reference_year"] > 2100):
            report.warn(f"population_statistics.id={row['id']}: implausible reference_year")

    for row in conn.execute("SELECT id, area_sq_km FROM area_statistics"):
        if row["area_sq_km"] < 0:
            report.error(f"area_statistics.id={row['id']}: negative area")


def check_source_provenance(conn: sqlite3.Connection, report: Report) -> None:
    """Records with a status beyond 'raw' should carry a source, except
    explicitly-labelled development fixtures."""
    for table in ADMIN_TABLES:
        try:
            rows = conn.execute(
                f"SELECT id, status, source_id FROM {table} WHERE status != 'raw'"
            ).fetchall()
        except sqlite3.OperationalError:
            continue
        for row in rows:
            if row["source_id"] is None:
                report.error(
                    f"{table}.id={row['id']}: status={row['status']!r} but no source_id set"
                )


CHECKS = [
    ("structural", check_structural),
    ("referential", check_referential),
    ("geographic", check_geographic),
    ("statistical", check_statistical),
    ("source provenance", check_source_provenance),
]


def main() -> int:
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    if not db_path.exists():
        print(f"No database at {db_path}. Run 'make build-db' first.", file=sys.stderr)
        return 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    report = Report()
    for name, check in CHECKS:
        before_errors = len(report.errors)
        check(conn, report)
        added = len(report.errors) - before_errors
        status = "FAIL" if added else "ok"
        print(f"[{status}] {name} validation ({added} error(s))")

    conn.close()

    if report.warnings:
        print("\nWarnings:")
        for w in report.warnings:
            print(f"  - {w}")

    if report.errors:
        print("\nErrors:")
        for e in report.errors:
            print(f"  - {e}")
        print(f"\nValidation FAILED: {len(report.errors)} error(s).")
        return 1

    print("\nValidation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
