# Kenya Data

[![CI](https://github.com/ToshGitonga0/kenya-data/actions/workflows/ci.yml/badge.svg)](https://github.com/ToshGitonga0/kenya-data/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A structured, validated, versioned, developer-friendly data layer for Kenya.

Kenya Data is an open-source project building a trusted data layer for
Kenyan administrative and geographic data — counties, constituencies,
wards, sub-counties, locations and sub-locations — distributed as a
portable SQLite database and consumed through native Python and
TypeScript SDKs.

```python
from kenya_data import Kenya

kenya = Kenya()
kenya.counties.list()
kenya.counties.get("Nakuru")
kenya.constituencies.in_county("Nakuru")
kenya.wards.in_constituency("Naivasha")
```

```typescript
import { Kenya } from "@kenya-data/core";

const kenya = new Kenya();
kenya.counties.list();
kenya.counties.get("Nakuru");
kenya.constituencies.inCounty("Nakuru");
```

## Status: real data, pending independent verification

This repository ships real Kenyan administrative data from day one:
all 47 counties, 290 constituencies, 1450 wards and 301 sub-counties,
sourced from the IEBC delimitation and KNBS census via the
[kenya-regions](https://github.com/nicanor-korir/kenya-regions)
aggregation — see [data/approved/README.md](data/approved/README.md)
for exactly where it came from. It has **not** yet been independently
re-verified by this project against the IEBC/KNBS originals, which is
why its source-registry entry is marked `validation_status:
under_review` rather than `validated`. See
[docs/data-research.md](docs/data-research.md) for what "verified"
means here and how that review (or a corrected/expanded dataset) gets
admitted into the project.

## Why this project exists

Kenyan public data is scattered across PDFs, inconsistent spreadsheets,
and websites with no versioning or provenance. Kenya Data's goal is a
single, well-modeled, source-attributed dataset that developers can
depend on the same way they depend on a package registry — with a
clear answer to "where did this number come from, and can I trust it?"

## Architecture

```
DATA SOURCES → RESEARCH → SOURCE REGISTRY → INGESTION → VALIDATION
    → APPROVED DATA → SQLITE (kenya.db) → Python SDK / TypeScript SDK
```

Full detail: [docs/architecture.md](docs/architecture.md).

## Research philosophy

No dataset is treated as correct merely because it exists online.
Every source is recorded in the [source registry](research/source-registry/),
evaluated against a documented [source hierarchy](docs/source-policy.md),
and — where sources disagree — the disagreement is written down in
[research/discrepancies/](research/discrepancies/) rather than
silently resolved. See [docs/data-research.md](docs/data-research.md).

## Data provenance

Every record in the approved dataset can answer: which source produced
this value, when was it retrieved, what year does it represent, what
transformations were applied, and who/what approved it. See
[docs/data-model.md](docs/data-model.md).

## Validation

Structural, referential, geographic, statistical, and source-provenance
checks run before any data is "approved." See
[docs/data-quality.md](docs/data-quality.md).

## Distribution: SQLite

The canonical distribution artifact is a single portable file,
`data/kenya.db`, generated from the validated pipeline — never hand-edited.
See [docs/data-model.md](docs/data-model.md).

## SDKs

- **Python** — `packages/python`, see [docs/sdk-design.md](docs/sdk-design.md)
- **TypeScript** — `packages/typescript`, see [docs/sdk-design.md](docs/sdk-design.md)

SDK version and dataset version are independent — see
[docs/versioning.md](docs/versioning.md).

## Installation

Not yet published to PyPI or npm. Until then, install from a local
checkout:

```bash
git clone https://github.com/ToshGitonga0/kenya-data.git
cd kenya-data
make build-db   # builds data/kenya.db from data/approved/
pip install -e packages/python
cd packages/typescript && npm install && npm run build
```

Once published (see [docs/publishing.md](docs/publishing.md)):

```bash
pip install kenya-data
npm install @kenya-data/core
```

## Development

```bash
make setup       # install SDK dependencies
make validate    # run the data validation framework
make build-db    # (re)build data/kenya.db from approved data
make test        # run Python + TypeScript test suites
make lint        # lint both SDKs
make format      # format both SDKs
make inspect-db  # open kenya.db in the sqlite3 CLI
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full research → validate
→ approve → publish workflow.

## Publishing

Nothing is published by this scaffold. See
[docs/publishing.md](docs/publishing.md) for the intended future release
flow.

## License

See [LICENSE](LICENSE).
