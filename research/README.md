# Research layer

This directory is where Kenyan data becomes *trustworthy* Kenyan data.
Nothing here is canonical yet — it is the working area for finding,
recording, and evaluating sources before anything is normalized,
validated, and approved into `data/approved/`.

Workflow: find source → record source → assess authority → extract
data → normalize → cross-check → document discrepancies →
resolve/document decision → approve → canonical dataset.

- `sources/` — raw notes and snapshots about candidate sources
- `source-registry/` — structured, reviewable source records (one file
  per source; see the template)
- `investigations/` — "what are we trying to establish, and why"
- `validation/` — validation run notes tied to specific research
- `discrepancies/` — formal records of conflicting data between sources
- `decisions/` — how a discrepancy or ambiguous case was resolved
- `reports/` — periodic summaries of research progress

See [docs/data-research.md](../docs/data-research.md) and
[docs/source-policy.md](../docs/source-policy.md).
