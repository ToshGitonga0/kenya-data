-- Kenya Data canonical schema.
--
-- This is the single source of truth for the shape of the approved
-- dataset. data/kenya.db is generated FROM this schema plus the
-- approved data — it is never hand-edited.
--
-- Hierarchy modeled directly via foreign keys rather than a generic
-- relationship table, so queries like "wards in a county" are plain
-- joins instead of graph traversal.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Dataset-level metadata
-- ---------------------------------------------------------------------

CREATE TABLE dataset_versions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    version         TEXT NOT NULL UNIQUE,   -- e.g. "2026.09"
    status          TEXT NOT NULL CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    description     TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE data_sources (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id             TEXT NOT NULL UNIQUE,  -- matches research/source-registry/<source_id>.yaml
    name                  TEXT NOT NULL,
    organization          TEXT,
    source_type           TEXT,
    source_url            TEXT,
    document_name         TEXT,
    publication_date      TEXT,
    retrieved_at          TEXT,
    reference_year        INTEGER,
    version               TEXT,
    license               TEXT,
    authority_level       TEXT CHECK (
                              authority_level IN ('primary', 'secondary', 'tertiary')
                          ),
    validation_status     TEXT NOT NULL DEFAULT 'unreviewed' CHECK (
                              validation_status IN ('unreviewed', 'under_review',
                                                     'validated', 'rejected')
                          ),
    methodology           TEXT,
    notes                 TEXT
);

-- ---------------------------------------------------------------------
-- Administrative hierarchy
-- ---------------------------------------------------------------------

CREATE TABLE counties (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,   -- stable external id, e.g. "KE-31"
    name            TEXT NOT NULL,
    capital         TEXT,
    source_id       INTEGER REFERENCES data_sources(id),
    dataset_version INTEGER NOT NULL REFERENCES dataset_versions(id),
    status          TEXT NOT NULL DEFAULT 'raw' CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE sub_counties (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    county_id       INTEGER NOT NULL REFERENCES counties(id),
    source_id       INTEGER REFERENCES data_sources(id),
    dataset_version INTEGER NOT NULL REFERENCES dataset_versions(id),
    status          TEXT NOT NULL DEFAULT 'raw' CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE constituencies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    county_id       INTEGER NOT NULL REFERENCES counties(id),
    source_id       INTEGER REFERENCES data_sources(id),
    dataset_version INTEGER NOT NULL REFERENCES dataset_versions(id),
    status          TEXT NOT NULL DEFAULT 'raw' CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE wards (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    code              TEXT NOT NULL UNIQUE,
    name              TEXT NOT NULL,
    constituency_id   INTEGER NOT NULL REFERENCES constituencies(id),
    sub_county_id     INTEGER REFERENCES sub_counties(id),
    source_id         INTEGER REFERENCES data_sources(id),
    dataset_version   INTEGER NOT NULL REFERENCES dataset_versions(id),
    status            TEXT NOT NULL DEFAULT 'raw' CHECK (
                          status IN ('raw', 'processed', 'validated',
                                     'approved', 'published', 'deprecated')
                      ),
    created_at        TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    ward_id         INTEGER NOT NULL REFERENCES wards(id),
    source_id       INTEGER REFERENCES data_sources(id),
    dataset_version INTEGER NOT NULL REFERENCES dataset_versions(id),
    status          TEXT NOT NULL DEFAULT 'raw' CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE sub_locations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    location_id     INTEGER NOT NULL REFERENCES locations(id),
    source_id       INTEGER REFERENCES data_sources(id),
    dataset_version INTEGER NOT NULL REFERENCES dataset_versions(id),
    status          TEXT NOT NULL DEFAULT 'raw' CHECK (
                        status IN ('raw', 'processed', 'validated',
                                   'approved', 'published', 'deprecated')
                    ),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- ---------------------------------------------------------------------
-- Geography
-- ---------------------------------------------------------------------

-- Point coordinates (e.g. a representative point for an entity),
-- distinct from polygon/boundary geometry below.
CREATE TABLE coordinates (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     TEXT NOT NULL CHECK (
                        entity_type IN ('county', 'constituency', 'ward',
                                        'sub_county', 'location', 'sub_location')
                    ),
    entity_id       INTEGER NOT NULL,
    latitude        REAL NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude       REAL NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    source_id       INTEGER REFERENCES data_sources(id),
    UNIQUE (entity_type, entity_id)
);

-- Polygon/boundary geometry, stored as GeoJSON text. Kept separate from
-- point coordinates deliberately (see docs/data-model.md).
CREATE TABLE boundaries (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     TEXT NOT NULL CHECK (
                        entity_type IN ('county', 'constituency', 'ward',
                                        'sub_county', 'location', 'sub_location')
                    ),
    entity_id       INTEGER NOT NULL,
    geojson         TEXT NOT NULL,  -- validated GeoJSON Polygon/MultiPolygon
    source_id       INTEGER REFERENCES data_sources(id),
    UNIQUE (entity_type, entity_id)
);

-- ---------------------------------------------------------------------
-- Statistics
-- ---------------------------------------------------------------------

CREATE TABLE population_statistics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     TEXT NOT NULL CHECK (
                        entity_type IN ('county', 'constituency', 'ward',
                                        'sub_county', 'location', 'sub_location')
                    ),
    entity_id       INTEGER NOT NULL,
    reference_year  INTEGER NOT NULL,
    population      INTEGER NOT NULL CHECK (population >= 0),
    source_id       INTEGER NOT NULL REFERENCES data_sources(id),
    UNIQUE (entity_type, entity_id, reference_year, source_id)
);

CREATE TABLE area_statistics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type     TEXT NOT NULL CHECK (
                        entity_type IN ('county', 'constituency', 'ward',
                                        'sub_county', 'location', 'sub_location')
                    ),
    entity_id       INTEGER NOT NULL,
    area_sq_km      REAL NOT NULL CHECK (area_sq_km >= 0),
    reference_year  INTEGER,
    source_id       INTEGER NOT NULL REFERENCES data_sources(id),
    UNIQUE (entity_type, entity_id, source_id)
);

-- ---------------------------------------------------------------------
-- Indexes
-- ---------------------------------------------------------------------

CREATE INDEX idx_sub_counties_county          ON sub_counties(county_id);
CREATE INDEX idx_constituencies_county        ON constituencies(county_id);
CREATE INDEX idx_wards_constituency           ON wards(constituency_id);
CREATE INDEX idx_wards_sub_county             ON wards(sub_county_id);
CREATE INDEX idx_locations_ward               ON locations(ward_id);
CREATE INDEX idx_sub_locations_location       ON sub_locations(location_id);
CREATE INDEX idx_coordinates_entity           ON coordinates(entity_type, entity_id);
CREATE INDEX idx_boundaries_entity            ON boundaries(entity_type, entity_id);
CREATE INDEX idx_population_entity            ON population_statistics(entity_type, entity_id);
CREATE INDEX idx_area_entity                  ON area_statistics(entity_type, entity_id);
