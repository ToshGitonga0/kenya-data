# kenya-data (Python SDK)

Install the published package:

```bash
pip install kenya-data
```

```python
from kenya_data import Kenya

kenya = Kenya()                       # loads the bundled data/kenya.db by default
kenya = Kenya(db_path="/path/to/kenya.db")  # or point at a specific build

kenya.counties.list()
kenya.counties.get("Nakuru")
kenya.constituencies.in_county("Nakuru")
kenya.wards.in_constituency("Naivasha")

kenya.dataset.version
kenya.dataset.updated_at
```

The package includes the SQLite database and is backed by the database built
from `database/schema/schema.sql` — see the repository root [README](../../README.md)
and [docs/sdk-design.md](../../docs/sdk-design.md).
