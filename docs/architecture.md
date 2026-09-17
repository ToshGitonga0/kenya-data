# Architecture

```
DATA SOURCES
     |
RESEARCH               (research/)
     |
SOURCE REGISTRY        (research/source-registry/)
     |
INGESTION              (scripts/import-data/  -> data/raw/)
     |
NORMALIZATION          (scripts/normalize-data/ -> data/processed/)
     |
VALIDATION             (scripts/validate-data/)
     |
APPROVED DATA          (data/approved/)
     |
CANONICAL SCHEMA       (database/schema/schema.sql)
     |
SQLITE                 (data/kenya.db)
    / \
Python SDK   TypeScript SDK
(packages/python)  (packages/typescript)
     \       /
     DEVELOPERS
```

## Why each layer exists

- **Research**: no data enters the pipeline without a documented
  source. This is what makes "where did this number come from"
  answerable later.
- **Source registry**: structured, comparable metadata about every
  source, so authority and recency can be judged consistently.
- **Ingestion**: keeps "what the source actually said" separate from
  any transformation, so mistakes in normalization are traceable and
  reversible.
- **Normalization**: converts heterogeneous source formats into the one
  shape the schema expects.
- **Validation**: catches structural, referential, geographic,
  statistical, and provenance problems before anything is approved.
- **Approved data**: the reviewed, trusted subset of processed data —
  distinct from raw/processed so "trusted" is never ambiguous.
- **Canonical schema**: one relational model, so the hierarchy
  (county -> constituency -> ward -> ...) is enforced by foreign keys,
  not by convention.
- **SQLite**: a single portable, queryable-without-a-server file that
  both SDKs read directly.
- **SDKs**: domain-shaped interfaces (`kenya.counties.get(...)`) rather
  than raw SQL, so the underlying schema can evolve without breaking
  every consumer.

See also [docs/data-model.md](data-model.md),
[docs/data-research.md](data-research.md), and
[docs/data-quality.md](data-quality.md).
