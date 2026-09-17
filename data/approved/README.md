# Approved data

`kenya_administrative.json` is real Kenyan administrative data: all
47 counties, 290 constituencies, 1450 wards, and 301 sub-counties,
plus 2009/2019 census population, area, and centroid coordinates for
counties and constituencies.

**Where it came from:** reformatted from the
[kenya-regions](https://github.com/nicanor-korir/kenya-regions) npm
package (MIT licensed), which itself aggregates and cross-checks the
IEBC county/constituency/ward hierarchy, OCHA's COD-AB admin1/admin2
layers, and the KNBS 2009/2019 censuses. Full provenance, including
the specific upstream files and known cross-source conflicts that
package resolved, is recorded in
[research/source-registry/kenya-regions-npm.yaml](../../research/source-registry/kenya-regions-npm.yaml).

**What "approved" means here, precisely:** every record in this file
carries `status: "approved"` and a `source_id` referencing that
registry entry, so it passes the source-provenance check in
`scripts/validate-data/validate.py`. It has **not** yet been
independently cross-checked by this project directly against the
IEBC/KNBS primary publications — the registry entry's
`validation_status` is deliberately `under_review`, not `validated`,
to reflect that. Tightening that (spot-checking against IEBC/KNBS
originals, or adding those primaries as their own registry entries)
is exactly the kind of task described in
[docs/data-research.md](../../docs/data-research.md) and
[research/investigations/](../../research/investigations/).

**What's intentionally not included yet:** locations, sub-locations,
boundary polygons, and any data beyond the 2019 census reference
year. `make build-db` loads exactly what's in this file — extending
it follows the same import → normalize → validate → approve pipeline
as any other future source.
