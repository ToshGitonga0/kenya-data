# SDK design

Both SDKs are thin, typed wrappers around read queries against
`data/kenya.db` — they do not expose raw SQL as the primary API.

## Shape

```python
kenya = Kenya()
kenya.counties.list()
kenya.counties.get("Nakuru")
kenya.constituencies.list()
kenya.constituencies.get("Naivasha")
kenya.constituencies.in_county("Nakuru")
kenya.wards.list()
kenya.wards.get("Biashara")
kenya.wards.in_constituency("Naivasha")
kenya.wards.in_county("Nakuru")     # traverses constituency -> ward
kenya.dataset.version
kenya.dataset.updated_at
```

```typescript
const kenya = new Kenya();
kenya.counties.list();
kenya.counties.get("Nakuru");
kenya.constituencies.list();
kenya.constituencies.get("Naivasha");
kenya.constituencies.inCounty("Nakuru");
kenya.wards.list();
kenya.wards.get("Biashara");
kenya.wards.inConstituency("Naivasha");
kenya.wards.inCounty("Nakuru");
kenya.dataset.version;
kenya.dataset.updatedAt;
```

## Conventions

- Lookups (`get`) accept either a `code` or a `name`
  (case-insensitive) and raise `EntityNotFoundError` when nothing
  matches — never return `None`/`undefined` silently.
- `list()` methods return plain arrays sorted by name.
- Hierarchy-traversal methods (`in_county`, `in_constituency`) resolve
  the parent first, so an unknown parent raises the same
  `EntityNotFoundError` as a direct lookup would.
- The default constructor resolves the bundled `data/kenya.db`
  relative to the package location; both SDKs also accept an explicit
  `db_path` / `dbPath`.
- Neither SDK ships a write API — the database is a read-only
  distribution artifact, built by `make build-db`.

## Adding a new entity type

1. Add the table to `database/schema/schema.sql`.
2. Add a model/type (`models.py` / `types.ts`).
3. Add a lookup class (`<entity>.py` / `<entity>.ts`) following the
   existing `Counties`/`Constituencies`/`Wards` pattern.
4. Wire it into `client.py` / `index.ts`.
5. Add fixture rows and tests.
