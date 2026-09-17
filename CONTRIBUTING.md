# Contributing to Kenya Data

Kenya Data grows through a deliberate research-to-publication pipeline.
No dataset enters the canonical database without going through it.

## The workflow

1. **Find a Kenyan dataset.** Government publications, official
   statutory bodies, or (clearly labelled as lower-authority) academic
   or commercial datasets.
2. **Document its source.** Add a source record to
   `research/source-registry/` — see
   [docs/source-policy.md](docs/source-policy.md) for the required
   fields. Never invent source metadata; if a field is unknown, mark it
   unknown.
3. **Add it to the research system.** Create an investigation note in
   `research/investigations/` describing what you're trying to
   establish and why this source is relevant.
4. **Build an importer.** Add a script under `scripts/import-data/`
   that reads the raw source into `data/raw/`.
5. **Normalize.** Add a script under `scripts/normalize-data/` that
   transforms raw data into the shape defined in
   [docs/data-model.md](docs/data-model.md), writing to
   `data/processed/`.
6. **Run validation.** `make validate` runs the checks described in
   [docs/data-quality.md](docs/data-quality.md).
7. **Document discrepancies.** If your source disagrees with an
   existing one, write a record in `research/discrepancies/` — do not
   silently overwrite the earlier value. Propose a resolution in
   `research/decisions/` if you believe one is warranted.
8. **Submit for review.** Open a pull request. Reviewers check source
   authority, validation results, and discrepancy handling.
9. **Add it to the approved dataset.** Once merged, the data moves to
   `data/approved/` with a `status: approved` marker (see
   [docs/data-model.md](docs/data-model.md) for the status lifecycle).
10. **Generate a new database release.** `make build-db` regenerates
    `data/kenya.db` from `data/approved/`.

## Ground rules

- **Never fabricate data.** No population figures, boundaries,
  statistics, source URLs, publication dates, or licenses that were not
  actually found in a real source.
- **Never silently overwrite conflicting data.** Record the conflict.
- **Development fixtures are not production data.** Keep them in
  `data/fixtures/` and clearly labelled.
- **Prefer primary sources.** See the source hierarchy in
  [docs/source-policy.md](docs/source-policy.md).

## Code contributions

- Python SDK: `packages/python` (pytest, type-checked).
- TypeScript SDK: `packages/typescript` (Node's built-in test runner, strict TypeScript).
- Run `make lint` and `make test` before opening a PR.

## Commit style

Small, reviewable commits. Prefix data-pipeline commits with the layer
they touch, e.g. `research:`, `data:`, `db:`, `sdk-py:`, `sdk-ts:`,
`docs:`.
