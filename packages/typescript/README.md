# @kenya-data/core (TypeScript SDK)

```typescript
import { Kenya } from "@kenya-data/core";

const kenya = new Kenya();                          // loads the bundled data/kenya.db
const kenya2 = new Kenya({ dbPath: "/path/to/kenya.db" });

kenya.counties.list();
kenya.counties.get("Nakuru");
kenya.constituencies.inCounty("Nakuru");
kenya.wards.inConstituency("Naivasha");

kenya.dataset.version;
kenya.dataset.updatedAt;
```

Backed by the SQLite database built from `database/schema/schema.sql`
via `better-sqlite3` — see the repository root
[README](../../README.md) and [docs/sdk-design.md](../../docs/sdk-design.md).
