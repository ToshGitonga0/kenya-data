#!/usr/bin/env python3
"""
Build a fresh SQLite database from database/schema/schema.sql and load
whatever is in data/approved/ into it.

data/approved/kenya_administrative.json ships with this scaffold
already populated with real Kenyan administrative data (47 counties,
290 constituencies, 1450 wards, 301 sub-counties, plus population,
area and centroid coordinates) — see
data/approved/README.md and research/source-registry/kenya-regions-npm.yaml
for exactly where it came from and what has (and has not) been
independently verified.

Usage:
    python3 database/seeds/load_approved_data.py [path/to/output.db]
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "database" / "schema" / "schema.sql"
APPROVED_PATH = REPO_ROOT / "data" / "approved" / "kenya_administrative.json"


def build(db_path: Path, dataset_path: Path = APPROVED_PATH) -> None:
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA_PATH.read_text())
    conn.execute("PRAGMA foreign_keys = ON")

    dataset = json.loads(dataset_path.read_text())
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO dataset_versions (version, status, description) VALUES (?, ?, ?)",
        (dataset["dataset_version"]["version"], dataset["dataset_version"]["status"],
         dataset["dataset_version"]["description"]),
    )
    dataset_version_id = cur.lastrowid

    source_ids: dict[str, int] = {}
    for src in dataset["sources"]:
        cur.execute(
            """INSERT INTO data_sources
               (source_id, name, organization, source_type, source_url, document_name,
                reference_year, version, license, authority_level, methodology, notes,
                validation_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (src["source_id"], src["name"], src.get("organization"), src.get("source_type"),
             src.get("source_url"), src.get("document_name"), src.get("reference_year"),
             src.get("version"), src.get("license"), src.get("authority_level"),
             src.get("methodology"), src.get("notes"),
             src.get("validation_status", "unreviewed")),
        )
        source_ids[src["source_id"]] = cur.lastrowid

    county_ids: dict[str, int] = {}
    for c in dataset["counties"]:
        cur.execute(
            """INSERT INTO counties (code, name, capital, source_id, dataset_version, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (c["code"], c["name"], c.get("capital"), source_ids.get(c.get("source_id")),
             dataset_version_id, c.get("status", "raw")),
        )
        county_ids[c["code"]] = cur.lastrowid

    constituency_ids: dict[str, int] = {}
    for co in dataset["constituencies"]:
        cur.execute(
            """INSERT INTO constituencies (code, name, county_id, source_id, dataset_version, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (co["code"], co["name"], county_ids[co["county_code"]],
             source_ids.get(co.get("source_id")), dataset_version_id,
             co.get("status", "raw")),
        )
        constituency_ids[co["code"]] = cur.lastrowid

    sub_county_ids: dict[str, int] = {}
    for sc in dataset.get("sub_counties", []):
        cur.execute(
            """INSERT INTO sub_counties (code, name, county_id, source_id, dataset_version, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (sc["code"], sc["name"], county_ids[sc["county_code"]],
             source_ids.get(sc.get("source_id")), dataset_version_id,
             sc.get("status", "raw")),
        )
        sub_county_ids[sc["code"]] = cur.lastrowid

    for w in dataset["wards"]:
        sub_county_id = sub_county_ids.get(w.get("sub_county_code")) if w.get("sub_county_code") else None
        cur.execute(
            """INSERT INTO wards (code, name, constituency_id, sub_county_id, source_id,
                                   dataset_version, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (w["code"], w["name"], constituency_ids[w["constituency_code"]], sub_county_id,
             source_ids.get(w.get("source_id")), dataset_version_id,
             w.get("status", "raw")),
        )

    entity_ids = {"county": county_ids, "constituency": constituency_ids}

    for p in dataset.get("population_statistics", []):
        ids = entity_ids[p["entity_type"]]
        cur.execute(
            """INSERT INTO population_statistics
               (entity_type, entity_id, reference_year, population, source_id)
               VALUES (?, ?, ?, ?, ?)""",
            (p["entity_type"], ids[p["entity_code"]], p["reference_year"], p["population"],
             source_ids[p["source_id"]]),
        )

    for a in dataset.get("area_statistics", []):
        ids = entity_ids[a["entity_type"]]
        cur.execute(
            """INSERT INTO area_statistics
               (entity_type, entity_id, area_sq_km, reference_year, source_id)
               VALUES (?, ?, ?, ?, ?)""",
            (a["entity_type"], ids[a["entity_code"]], a["area_sq_km"], a.get("reference_year"),
             source_ids[a["source_id"]]),
        )

    for pt in dataset.get("coordinates", []):
        ids = entity_ids[pt["entity_type"]]
        cur.execute(
            """INSERT INTO coordinates (entity_type, entity_id, latitude, longitude, source_id)
               VALUES (?, ?, ?, ?, ?)""",
            (pt["entity_type"], ids[pt["entity_code"]], pt["latitude"], pt["longitude"],
             source_ids[pt["source_id"]]),
        )

    conn.commit()
    conn.close()
    print(f"Loaded {dataset_path.name} ({dataset['dataset_version']['version']}) into {db_path}")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "data" / "kenya.db"
    out.parent.mkdir(parents=True, exist_ok=True)
    build(out)
