# Publishing

This documents the intended future release flow.

```
Research
  -> Validate            (make validate)
  -> Approve             (data moved into data/approved/, reviewed)
  -> Build dataset       (normalize approved data)
  -> Build SQLite         (make build-db)
  -> Run tests            (make test)
  -> Build Python SDK      (python3 -m build, from packages/python)
  -> Build TypeScript SDK  (npm run build, from packages/typescript)
  -> Version               (bump SDK and/or dataset versions per docs/versioning.md)
  -> Publish Python package (twine upload, manual)
  -> Publish npm package    (npm publish, manual)
```

Both the Python package build/publish and the npm package
build/publish are manual, deliberate actions taken by a maintainer —
this repository does not include CI automation that publishes
packages.
