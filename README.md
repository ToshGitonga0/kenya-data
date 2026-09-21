# Kenya Data

[![CI](https://github.com/ToshGitonga0/kenya-data/actions/workflows/ci.yml/badge.svg)](https://github.com/ToshGitonga0/kenya-data/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![npm](https://img.shields.io/npm/v/kenya-data-core)](https://www.npmjs.com/package/kenya-data-core)
[![PyPI](https://img.shields.io/pypi/v/kenya-data)](https://pypi.org/project/kenya-data/)

> A structured, versioned, and developer-friendly data layer for Kenya.

**Kenya Data** provides structured Kenyan administrative and geographic data through a portable SQLite database and native Python and TypeScript SDKs.

The project currently provides:

* **47 counties**
* **290 constituencies**
* **1,450 wards**
* County → constituency relationships
* Constituency → ward relationships
* Stable identifiers and codes
* Dataset version and update metadata
* A bundled, read-only SQLite database
* Native Python and TypeScript APIs

The same dataset is distributed across both SDKs, allowing developers to work with Kenya's administrative geography without maintaining their own CSV files, spreadsheets, database imports, or scraping pipelines.

---

## Current Release

### SDKs

| Package    | Registry | Version |
| ---------- | -------- | ------: |
| Python     | PyPI     | `0.1.1` |
| TypeScript | npm      | `0.1.1` |

Install directly from the public package registries:

```bash
pip install kenya-data
```

```bash
npm install kenya-data-core
```

### Dataset

```text
Version: 2026.09-iebc2012-knbs2019
Status: approved
Updated: 2026-09-20 18:59:13
```

The SDK version and dataset version are intentionally separate. A package release identifies the SDK, while the dataset version identifies the underlying data snapshot.

---

# Quick Start

## Python

```python
from kenya_data import Kenya

kenya = Kenya()

print(kenya.counties.list())
print(kenya.counties.get("Nakuru"))
print(kenya.constituencies.in_county("Nakuru"))
print(kenya.wards.in_constituency("Naivasha"))

kenya.close()
```

---

## TypeScript

```typescript
import { Kenya } from "kenya-data-core";

const kenya = new Kenya();

console.log(kenya.counties.list());
console.log(kenya.counties.get("Nakuru"));
console.log(kenya.constituencies.inCounty("Nakuru"));
console.log(kenya.wards.inConstituency("Naivasha"));

kenya.close();
```

---

# What You Get

Kenya Data is designed around a simple administrative hierarchy:

```text
Kenya
│
├── Counties (47)
│   │
│   └── Constituencies (290)
│       │
│       └── Wards (1,450)
│
└── Dataset metadata
```

Each level has stable identifiers and relationships to the level above it.

For example:

```text
Nairobi County
    │
    ├── Dagoretti North
    ├── Dagoretti South
    ├── Embakasi Central
    ├── Embakasi East
    ├── Embakasi North
    ├── Embakasi South
    ├── Embakasi West
    ├── Kamukunji
    ├── Kasarani
    ├── Kibra
    ├── Langata
    ├── Makadara
    ├── Mathare
    ├── Roysambu
    ├── Ruaraka
    ├── Starehe
    └── Westlands
```

Nairobi contains **17 constituencies**, and those relationships are represented directly in the dataset.

---

# API Overview

## Counties

### List all counties

Python:

```python
kenya.counties.list()
```

TypeScript:

```typescript
kenya.counties.list();
```

Returns all **47 counties**.

### Get a county

Python:

```python
kenya.counties.get("Nairobi")
```

TypeScript:

```typescript
kenya.counties.get("Nairobi");
```

County records include fields such as:

```text
id
code
name
capital
status
```

Example:

```text
id: 47
code: KE047
name: Nairobi
capital: Nairobi
status: approved
```

---

## Constituencies

### List all constituencies

Python:

```python
kenya.constituencies.list()
```

TypeScript:

```typescript
kenya.constituencies.list();
```

Returns all **290 constituencies**.

### Get a constituency

Python:

```python
kenya.constituencies.get("Naivasha")
```

TypeScript:

```typescript
kenya.constituencies.get("Naivasha");
```

### Get constituencies within a county

Python:

```python
kenya.constituencies.in_county("Nairobi")
```

TypeScript:

```typescript
kenya.constituencies.inCounty("Nairobi");
```

County names and county codes can be used for relationship queries where supported.

---

## Wards

### List all wards

Python:

```python
kenya.wards.list()
```

TypeScript:

```typescript
kenya.wards.list();
```

Returns all **1,450 wards**.

### Get a ward

Python:

```python
kenya.wards.get("Ward Name")
```

TypeScript:

```typescript
kenya.wards.get("Ward Name");
```

### Get wards within a constituency

Python:

```python
kenya.wards.in_constituency("Naivasha")
```

TypeScript:

```typescript
kenya.wards.inConstituency("Naivasha");
```

### Get wards within a county

Python:

```python
kenya.wards.in_county("Nakuru")
```

TypeScript:

```typescript
kenya.wards.inCounty("Nakuru");
```

---

# Dataset Metadata

The dataset exposes its own version and update information.

Python:

```python
print(kenya.dataset.version)
print(kenya.dataset.updated_at)
print(kenya.dataset.info())
```

TypeScript:

```typescript
console.log(kenya.dataset.version);
console.log(kenya.dataset.updatedAt);
console.log(kenya.dataset.info());
```

Current dataset:

```text
Version: 2026.09-iebc2012-knbs2019
Status: approved
Updated: 2026-09-20 18:59:13
```

This makes it possible for applications to identify exactly which dataset snapshot they are using.

---

# Data Integrity

The published release has been tested as a real external consumer installation from both package registries.

### TypeScript / npm

The published `kenya-data-core@0.1.1` package was installed into a clean environment directly from npm.

Verified:

* 47 counties
* 290 constituencies
* 1,450 wards
* Bundled SQLite database loads successfully
* Dataset metadata is available
* Nairobi resolves correctly
* Nairobi contains 17 constituencies
* Every constituency references an existing county
* Every ward references an existing constituency

### Python / PyPI

The published `kenya-data==0.1.1` package was installed into a clean Python virtual environment directly from PyPI.

Verified:

* 47 counties
* 290 constituencies
* 1,450 wards
* Bundled SQLite database loads successfully
* Dataset metadata matches the TypeScript distribution
* Nairobi resolves correctly
* Nairobi contains 17 constituencies
* Every constituency references an existing county
* Every ward references an existing constituency

Relationship validation returned:

```text
Constituencies with invalid county: 0
Wards with invalid constituency: 0
```

The npm and PyPI distributions therefore expose the same underlying dataset and administrative relationships.

---

# Data Provenance

Kenya Data is designed around explicit data provenance rather than treating an online dataset as authoritative simply because it exists.

The project documents:

* Data sources
* Source retrieval information
* Dataset versions
* Transformations
* Validation procedures
* Data-model decisions
* Known discrepancies
* Approval status

The current dataset incorporates Kenyan administrative and geographic information derived from documented sources including IEBC delimitation data and KNBS census data.

See:

* [Data research](docs/data-research.md)
* [Source policy](docs/source-policy.md)
* [Source registry](research/source-registry/)
* [Approved data](data/approved/)

---

# Architecture

The project follows a pipeline from source material to developer-facing packages:

```text
DATA SOURCES
     │
     ▼
RESEARCH
     │
     ▼
SOURCE REGISTRY
     │
     ▼
INGESTION
     │
     ▼
VALIDATION
     │
     ▼
APPROVED DATA
     │
     ▼
SQLite (kenya.db)
     │
     ├───────────────┐
     ▼               ▼
 Python SDK      TypeScript SDK
     │               │
     ▼               ▼
   PyPI             npm
```

The SQLite database is the common distribution layer used by both SDKs.

More detail:

* [Architecture](docs/architecture.md)
* [Data model](docs/data-model.md)
* [Data quality](docs/data-quality.md)
* [SDK design](docs/sdk-design.md)

---

# Why SQLite?

Kenya Data uses SQLite as its canonical distribution format because it is:

* Portable
* Serverless
* Self-contained
* Easy to inspect
* Suitable for local applications
* Easy to bundle inside language packages
* Independent of an external database server

A developer can install the package and start querying the data immediately.

No database server is required.

No API key is required.

No network request is required for ordinary queries.

The published packages contain the database required to use the core dataset.

---

# Who Is This For?

Kenya Data is intended for developers and researchers building applications that need structured Kenyan geographic or administrative data.

Examples include:

* Kenyan address and location systems
* Data collection applications
* Government and civic technology
* Analytics platforms
* Research projects
* Mapping applications
* Web scraping pipelines
* Data engineering projects
* Statistical applications
* Administrative dashboards
* Geographic filtering
* County and constituency selectors
* Offline-first applications
* Prototypes and developer tools

Instead of maintaining a custom copy of Kenyan administrative data, an application can depend on a versioned package.

---

# Installation

## Python

Requires Python 3.9+.

```bash
pip install kenya-data
```

Verify:

```bash
python -c "from kenya_data import Kenya; print(len(Kenya().counties.list()))"
```

Expected:

```text
47
```

---

## TypeScript / JavaScript

Install with npm:

```bash
npm install kenya-data-core
```

Verify the package:

```bash
npm list kenya-data-core
```

Use it:

```typescript
import { Kenya } from "kenya-data-core";

const kenya = new Kenya();

console.log(kenya.counties.list().length);

kenya.close();
```

Expected:

```text
47
```

---

# Local Development

Clone the repository:

```bash
git clone https://github.com/ToshGitonga0/kenya-data.git
cd kenya-data
```

Install development dependencies:

```bash
make setup
```

Build the database:

```bash
make build-db
```

Run validation:

```bash
make validate
```

Run tests:

```bash
make test
```

Run linting:

```bash
make lint
```

Format the project:

```bash
make format
```

Inspect the SQLite database:

```bash
make inspect-db
```

---

# Project Structure

```text
kenya-data/
│
├── data/
│   ├── approved/
│   └── kenya.db
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── data-quality.md
│   ├── data-research.md
│   ├── publishing.md
│   ├── sdk-design.md
│   └── source-policy.md
│
├── packages/
│   ├── python/
│   └── typescript/
│
├── research/
│   ├── discrepancies/
│   └── source-registry/
│
├── tests/
│
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

# Versioning

Kenya Data has two independent versioning layers.

### SDK version

The package release version.

Examples:

```text
kenya-data 0.1.1
kenya-data-core 0.1.1
```

### Dataset version

The version of the underlying data snapshot.

Example:

```text
2026.09-iebc2012-knbs2019
```

This distinction allows the dataset to evolve independently from SDK implementation changes.

See [docs/versioning.md](docs/versioning.md).

---

# Contributing

Contributions are welcome.

Depending on the change, contributions may involve:

1. Research
2. Source documentation
3. Data transformation
4. Validation
5. Tests
6. Documentation
7. SDK implementation

Changes to the dataset should preserve provenance and validation information.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

---

# Published Packages

### Python

**PyPI:** `kenya-data`

```bash
pip install kenya-data
```

[View on PyPI](https://pypi.org/project/kenya-data/)

### TypeScript

**npm:** `kenya-data-core`

```bash
npm install kenya-data-core
```

[View on npm](https://www.npmjs.com/package/kenya-data-core)

---

# License

Kenya Data is released under the MIT License.

See [LICENSE](LICENSE) for the full license text.

---

## Project

**Repository:**
https://github.com/ToshGitonga0/kenya-data

**Python package:**
https://pypi.org/project/kenya-data/

**TypeScript package:**
https://www.npmjs.com/package/kenya-data-core
