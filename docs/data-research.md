# Data research

No dataset is treated as correct merely because it exists online.

## Workflow

```
Find source -> Record source -> Assess authority -> Extract data
  -> Normalize -> Cross-check -> Document discrepancies
  -> Resolve/document decision -> Approve -> Canonical dataset
```

1. **Find a source.** A government publication, statutory body
   dataset, academic study, or (lowest priority) a commercial or
   community dataset.
2. **Record it** as a `research/source-registry/<id>.yaml` entry (see
   the template in that directory) — every field either filled in with
   something actually verified, or left `null`.
3. **Assess its authority** against [docs/source-policy.md](source-policy.md).
4. **Extract** the raw values via an importer in `scripts/import-data/`.
5. **Normalize** via `scripts/normalize-data/` into the schema shape.
6. **Cross-check** against any existing data for the same entities.
7. **Document discrepancies** in `research/discrepancies/` — never
   silently pick a winner.
8. **Resolve or document a decision** in `research/decisions/` when a
   discrepancy needs a judgment call.
9. **Approve**: once validation passes and review is complete, the data
   moves into `data/approved/`.
10. It's now part of the **canonical dataset** the next `make build-db`
    will include.

## What counts as "verified"

A value is considered verified for this project's purposes when it (a)
has a recorded source in the registry, (b) has passed the automated
checks in `scripts/validate-data/validate.py`, and (c) has been
reviewed by a contributor other than the one who added it. Until then
it stays at `raw` or `processed` status and does not ship in a tagged
dataset release.
