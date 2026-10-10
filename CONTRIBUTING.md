# Contributing

This is a single-maintainer portfolio lab, run with the same discipline as a team repository.

1. Open or pick an issue. Every change is traceable to an issue.
2. Branch from `main` using `type/<issue>-short-slug` (see `docs/04-conventions.md`).
3. Commit with Conventional Commits (`feat(uc): add UC-012 cross-border CID`).
4. Open a PR, complete the checklist, wait for CI to pass.
5. Self-review after at least one pause (review the diff the next day, not in the same session).
6. Squash-merge. Update `CHANGELOG.md` when the change is user-visible.

Any artefact claiming a test result must reference evidence in the test matrix (`testing/test-matrix.csv`). No evidence, no "PASS".
