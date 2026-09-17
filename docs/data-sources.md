# Data sources

This file indexes the sources actually recorded in
`research/source-registry/`.

## kenya-regions (secondary, under review)

Backs everything currently in `data/approved/kenya_administrative.json`
(47 counties, 290 constituencies, 1450 wards, 301 sub-counties,
2009/2019 census population, area, centroid coordinates). Registry
entry: [research/source-registry/kenya-regions-npm.yaml](../research/source-registry/kenya-regions-npm.yaml).
Full detail on what it aggregates (IEBC hierarchy, OCHA COD-AB, KNBS
census, Constitution 2010) and what's still pending independent
verification: [data/approved/README.md](../data/approved/README.md).

See [docs/data-research.md](data-research.md) for how to add the next
source — including one that lets this project mark the kenya-regions
entry `validated` instead of `under_review`.
