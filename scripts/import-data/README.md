# Import scripts

Each source gets its own importer here (e.g. `knbs_census_2019.py`)
that reads the raw source file/URL and writes a plain, unnormalized
snapshot into `data/raw/`. Importers should not transform or validate
data — that happens in `scripts/normalize-data/` and
`scripts/validate-data/`. Reference the source's registry id from
`research/source-registry/` in a comment at the top of the importer.
