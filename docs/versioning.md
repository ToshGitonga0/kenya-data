# Versioning

Two independent version numbers:

```
Python SDK:      packages/python/pyproject.toml   -> project.version
TypeScript SDK:  packages/typescript/package.json -> version
Kenya dataset:   database dataset_versions.version, e.g. "2026.09"
```

The dataset is versioned by year and month of release
(`YYYY.MM`), independent of SDK semantic versions. An SDK release with
no dataset changes bumps only the SDK version; a new dataset release
(new sources, corrected values, newly approved entities) bumps
`dataset_versions.version` and is exposed to consumers via
`kenya.dataset.version` / `kenya.dataset.updated_at` (Python) and
`kenya.dataset.version` / `kenya.dataset.updatedAt` (TypeScript) —
never hardcoded in SDK source.

This split exists because an SDK bugfix should not force every
consumer to also pull a new dataset build, and vice versa.
