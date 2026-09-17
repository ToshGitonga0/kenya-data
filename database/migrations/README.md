# Migrations

`0001_initial.sql` is the current schema in migration form. As the
schema evolves, add `NNNN_description.sql` files here containing only
the incremental DDL (ALTER TABLE, new CREATE TABLE, etc.) — do not edit
`0001_initial.sql` after it has shipped.

`database/schema/schema.sql` should always reflect the cumulative
result of applying every migration in order, so a fresh database can be
built either by replaying migrations or by loading `schema.sql`
directly (this is what `make build-db` does today, since there is only
one migration so far).
