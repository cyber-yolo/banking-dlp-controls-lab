# Conventions

## Identifiers

| Object | Pattern | Example |
|---|---|---|
| Data category | `DC-##` | DC-04 |
| Control objective | `CO-##` | CO-02 |
| Use case | `UC-###` | UC-001 |
| Purview policy | `PV-POL-###` | PV-POL-001 |
| Purview rule | `PV-POL-###-R#` | PV-POL-001-R2 |
| Symantec policy | `SY-POL-###` | SY-POL-001 |
| Test case | `TC-###` | TC-003 |
| Generator scenario | `SCN-###` | SCN-002 |
| Regulatory mapping row | `RM-##` | RM-10 |
| Exception | `EXC-YYYY-###` | EXC-2026-004 |
| Indicators | `KPI-##`, `KRI-##` | KRI-02 |
| Evidence | `EV-<TC>-<yyyymmdd>-#` | EV-TC-001-20261015-1 |

In the lab tenant, prefix every object name with its ID (`PV-POL-001 External email - bank account data`) so evidence maps to specs without ambiguity.

## Files

Lowercase, hyphen-separated, IDs uppercase: `UC-001.yaml`, `test-strategy.md`.

## Git workflow

Trunk-based with short-lived branches, adapted to a single maintainer with structured review.

| Item | Convention |
|---|---|
| Default branch | `main`, protected by a ruleset: PR required, status checks required (`lint`, `test`, `secrets`), no force push, no deletion |
| Branches | `feat/<issue>-slug`, `fix/<issue>-slug`, `docs/<issue>-slug`, `test/<issue>-slug`, `chore/<issue>-slug` |
| Commits | Conventional Commits with scope: `feat(purview): add PV-POL-002 endpoint egress`, `test(uc-001): record TC-001 lab run` |
| Merge | Squash merge, PR title becomes the commit |
| Releases | Tag `v0.x.0` at the end of each milestone, release notes from `CHANGELOG.md` |
| Repository settings | Secret scanning and push protection on, private vulnerability reporting on, Dependabot alerts on |

Commit history matters: push work as it is done, milestone by milestone, with lab evidence in between. A repository created in one commit shows nothing about how the work was done.
