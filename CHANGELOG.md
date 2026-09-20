# Changelog

All notable changes to this project are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

Note: this file tracks the **project** (code, schema, SDKs). Dataset
releases are versioned separately — see
[docs/versioning.md](docs/versioning.md).

## [0.1.0] - 2026-09-20

### Added
- Initial public release of the Kenya Data project.
- Research layer, source registry, validation framework, and discrepancy tracking.
- Canonical SQLite schema and generated `data/kenya.db` distribution artifact.
- Python SDK skeleton under `packages/python`.
- TypeScript SDK skeleton under `packages/typescript`.
- Kenyan administrative data covering 47 counties, 290 constituencies,
  1,450 wards, and 301 sub-counties.
- Provenance and validation documentation, contributor guidance, and CI.

### Known limitations
- The current dataset is sourced from the `kenya-regions` aggregation and is
  marked `validation_status: under_review`; it has not yet been independently
  re-verified against the IEBC/KNBS primary publications.
- Locations, sub-locations, boundary polygons, and data beyond the 2019 census
  reference year are not included yet.
- Python and TypeScript packages are not yet published to PyPI or npm.

## [Unreleased]

Future changes will be documented here.
