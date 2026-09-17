# Data quality

`scripts/validate-data/validate.py` runs five categories of checks
against a built database. `make validate` runs it against
`data/kenya.db`.

## Structural validation
- Required fields present (`code`, `name`) on every administrative row
- No duplicate `code` values within a table
- (Enforced separately by the schema) unique identifiers, non-null
  foreign keys, and `status` restricted to the documented lifecycle
  values

## Referential validation
- Every `sub_counties.county_id`, `constituencies.county_id`,
  `wards.constituency_id`, `locations.ward_id`, and
  `sub_locations.location_id` must reference a row that exists — the
  check reports any orphaned child.

## Geographic validation
- Latitude within [-90, 90], longitude within [-180, 180]
- Warns (does not fail) when multiple distinct entities share the
  exact same point, since that's often a sign of a placeholder
  coordinate rather than real data

## Statistical validation
- Population and area values must be non-negative
- Warns on population records with implausible reference years

## Source validation
- Any administrative row with `status` beyond `raw` must carry a
  `source_id` — data cannot be silently treated as more trustworthy
  than its provenance supports

Warnings do not fail the build; errors do. Add new checks to
`scripts/validate-data/validate.py` as the dataset grows (e.g. checks
that compare a new source's values against existing approved values
and route disagreements into `research/discrepancies/`).
