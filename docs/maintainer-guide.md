# Maintainer guide

This project is intentionally conservative when it comes to data. The maintainers are responsible for keeping the pipeline trustworthy and reviewable.

## Working rules

- `main` is protected and is only updated through pull requests.
- Contributors should work from feature branches or forks.
- A source registry entry is required before new canonical data is approved.
- Data updates must be reviewed for provenance, validation, and scope.
- Do not merge unreviewed data or silent overwrites for conflicting records.

## Typical contributor flow

1. Open or pick an issue.
2. Create a branch or fork from `main`.
3. Do the smallest change that solves the problem.
4. Run the relevant validation before opening a pull request.
5. Submit the PR with the checklist that records provenance and validation steps.
6. Request review from a maintainer or a qualified reviewer.
7. Merge only after CI and review requirements are satisfied.

## Responsibilities for maintainers

- Keep the source policy and validation rules visible and enforced.
- Review the provenance of any data addition.
- Make sure the issue backlog describes bounded, reviewable work.
- Prefer small Pull Requests over large, multi-purpose changes.
- Keep branches focused on a single source, dataset, or schema concern.

## Release discipline

- Publish SDK releases separately from dataset releases where needed.
- Keep dataset changes tied to a verified source and a documented approval path.
- Review generated database artifacts and validation output when data changes are merged.
- Only mark data as approved after review and validation.
