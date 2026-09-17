# Development fixtures

This scaffold ships real Kenyan administrative data in
`data/approved/` (see `data/approved/README.md`), so nothing here is
needed to run `make build-db` or the SDK test suites — they run
against the real 47 counties / 290 constituencies / 1450 wards
directly.

Use this directory only if you need a deliberately tiny, synthetic
dataset for a specific edge case (e.g. exercising an importer against
a malformed record). Anything placed here must stay clearly labelled
as a fixture and must never be copied into `data/approved/`.
