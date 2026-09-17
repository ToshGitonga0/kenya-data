# Data model

## Administrative hierarchy

Modeled as direct foreign keys rather than a generic relationship
table, so the natural hierarchy is enforced by the schema itself and
queries stay simple joins:

```
County -> Sub-county -> Ward -> Location -> Sub-location
County -> Constituency -> Ward
```

A ward has a required `constituency_id` and an optional
`sub_county_id`, reflecting that Kenya's two administrative hierarchies
(the county/sub-county/location/sub-location line used for
administration, and the county/constituency line used for
representation) both bottom out at wards, but a ward's presence in one
does not require the other to be populated yet.

Tables: `counties`, `sub_counties`, `constituencies`, `wards`,
`locations`, `sub_locations`. Each stable external identifier is a
`code`, not the autoincrementing `id`, so codes can be referenced from
research and fixture files independent of database rebuilds.

## Status lifecycle

Every administrative-hierarchy row carries a `status`:

```
raw -> processed -> validated -> approved -> published -> (deprecated)
```

Only `data/approved/` content should reach `approved`/`published`
status in a real (non-fixture) database build. The validation
framework (`scripts/validate-data/validate.py`) checks that anything
past `raw` has a `source_id`.

## Geography

Two distinct concepts, intentionally in separate tables:

- `coordinates` — a single representative point per entity (lat/lon).
- `boundaries` — polygon/multipolygon geometry, stored as GeoJSON text.

This keeps "where is a pin for this place" separate from "what is this
place's exact shape," since they're populated independently and one
can exist without the other.

## Statistics

`population_statistics` and `area_statistics` are keyed by
`(entity_type, entity_id, reference_year, source_id)` (population) or
`(entity_type, entity_id, source_id)` (area) rather than a single
column on the entity table, because the same entity legitimately has
different population figures for different years and different
sources — see [docs/data-quality.md](data-quality.md) and
[research/discrepancies/](../research/discrepancies/).

## Provenance

`data_sources` mirrors the fields in a
`research/source-registry/*.yaml` entry. Every entity and statistic
that isn't a development fixture should carry a `source_id` once past
`raw` status, so any value in the database can be traced back to
`research/source-registry/` for full context (URL, retrieval date,
authority level, license, etc.).

## Dataset versioning

`dataset_versions` records the dataset (not SDK) release history —
see [docs/versioning.md](versioning.md).
