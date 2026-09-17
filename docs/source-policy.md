# Source policy

## Authority hierarchy

```
Primary / official
  - Government publications (e.g. Kenya Gazette notices)
  - Official government datasets (e.g. KNBS releases)
  - Official statutory bodies (e.g. IEBC boundary delimitation reports)

Secondary
  - Academic research
  - Established research organizations

Tertiary
  - Commercial datasets
  - Community-maintained datasets
  - Unverified websites
```

A source's `authority_level` in the registry must be one of `primary`,
`secondary`, or `tertiary`. Higher authority does not automatically win
a discrepancy — it is evidence to weigh, recorded alongside the
decision in `research/decisions/`, not a rule that shortcuts review.

## Required registry fields

See `research/source-registry/TEMPLATE.yaml`. In short: source name,
organization, source type, URL, document/dataset name, publication
date, retrieval date, geographic scope, administrative level,
reference year, version, license, authority level, methodology, notes,
and validation status.

## Rules

- Never invent a value for a registry field — use `null` for anything
  not actually verified.
- Never assign `authority_level: primary` to a source that is not an
  official government or statutory publication.
- Record `retrieved_at` at the time you actually fetched the source,
  not the publication date.
- If a source's license is unclear, mark it `null` and note the
  ambiguity — do not assume permissive licensing.
