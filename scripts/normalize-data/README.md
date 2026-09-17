# Normalization scripts

Each normalizer reads a specific file from `data/raw/`, transforms it
into the shape defined in `database/schema/schema.sql`
(`docs/data-model.md`), and writes to `data/processed/`. Keep
normalizers pure — no network access, no writing outside
`data/processed/`.
