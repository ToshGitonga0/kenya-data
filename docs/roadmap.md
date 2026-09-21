## Roadmap

This document is intentionally narrow and high-signal. It describes the next work that makes the dataset more trustworthy and easier for contributors to work on.

### Priority 1: source verification and trust

- Verify the existing county, constituency, and ward hierarchy against primary sources.
- Add or tighten source registry records for the approved dataset.
- Document discrepancies and decisions for conflicting values.
- Use the validation checks to catch or prevent regressions.

### Priority 2: missing administrative layers

- Research and add locations and sub-locations as authoritative sources become available.
- Confirm the relationship integrity between county, sub-county, constituency, ward, and location records.
- Add validation checks for missing or orphaned parent-child links.

### Priority 3: geography and boundaries

- Research boundary and polygon data sources.
- Evaluate licensing, update cadence, and geometry validity.
- Add geometry-specific validation once a source is approved.

### Priority 4: statistics and temporal coverage

- Add research for post-2019 population and administrative statistics.
- Record all statistics with reference year, source, and provenance.
- Keep dataset additions small, reviewable, and tied to a source registry entry.

### Priority 5: SDK and usability improvements

- Expose new approved fields consistently in Python and TypeScript.
- Add common query helpers and examples.
- Prioritize parity between the two SDKs.

## Working policy

- Data work starts only after a source registry record exists.
- Approved data changes are reviewed before merge.
- Keep PRs small and tied to a single source or schema concern.
- Do not broaden scope during a data-review task unless the source clearly requires it.
