# Roadmap

| Version | Objective | Main deliverables | Key issues | Depends on | Main risk | Acceptance criteria | Priority |
|---|---|---|---|---|---|---|---|
| 0.1 | Positioning, structure, security, taxonomy | README, SECURITY, CI, `.gitignore`, taxonomy, data catalog | #5 to #9 | none | Scope creep | CI green; taxonomy covers the 21 categories; validator passes | P1 |
| 0.2 | Use cases and first Purview scenarios | UC catalog (15), 4 detailed UC sheets, PV-POL-001 spec | #10 to #13 | 0.1 | Generic use cases | Each UC has thresholds, positive, negative and boundary tests defined | P1 |
| 0.3 | SITs, classification, Purview policies | Custom SIT rule pack imported in lab, sensitivity labels, PV-POL-001/003 in simulation | #14 to #17 | 0.2, lab tenant | Licensing gaps | SIT test (Test-DataClassification or portal test) evidenced; policies in S1 | P1 |
| 0.4 | Endpoint DLP, alerts, investigation | PV-POL-002 endpoint egress, alert configuration, triage run on lab alerts | #18 to #20 | 0.3, VM onboarded | Endpoint onboarding friction | USB, print, browser upload tests executed with evidence | P1 |
| 0.5 | Synthetic generator and test matrix | Generator v1, 12 scenarios, test matrix populated | #21 to #23 | 0.2 | Checksum realism vs safety | All positive/negative/boundary tests for PV-POL-001 run and recorded | P1 |
| 0.6 | Governance, exceptions, KPI/KRI, audit evidence | Lifecycle, RACI, playbook, exception register, KPI sheet computed from lab data | #24 to #26 | 0.4, 0.5 | Theory without data | At least 5 KPIs computed from real lab events | P2 |
| 0.7 | Regulatory mapping CH and LU | Mapping with every reference checked against the official text | #27, #28 | 0.1 | Wrong or outdated references | No row left TO VERIFY; requirement and control columns separated | P2 |
| 0.8 | Automation and regression | Config export script, regression runner, CI hardening | #29, #30 | 0.5 | Brittle scripts | Regression set replayable in under 1 hour with diff report | P2 |
| 0.9 | Symantec DLP extension | SY-POL specs for UC-001/003/004/010, comparison matrix completed | #31 | 0.5 | No lab: paper-only | Matrix states coverage, limits and test status per UC | P2 |
| 1.0 | Documented multi-vendor framework | Release, executive summary refreshed, walkthrough video or GIF | #32 | all | Overclaiming | Every "tested" claim has evidence; limits page up to date | P1 |

## Implementation order (first files)

1. `README.md`, `SECURITY.md`, `.gitignore`, `.gitleaks.toml`, `.github/workflows/ci.yml`
2. `data-classification/taxonomy.yaml`, `data-classification/data-catalog.csv`
3. `docs/01-architecture.md` (control objectives), `docs/02-assumptions-and-limits.md`
4. `use-cases/catalog.csv`, `use-cases/UC-001.yaml`
5. `synthetic-data-generator/` (values, render, manifest, tests)
6. `platforms/microsoft-purview/policies/PV-POL-001.yaml`, `testing/test-cases/TC-001..003`
7. Lab run of PV-POL-001 in simulation, first evidence, then the rest of the backlog.

## Success criteria for v1.0

- At least 6 use cases fully tested on Purview with positive, negative and boundary evidence.
- At least one policy taken through S1 to S4 with a documented tuning decision (before/after false positive rate).
- Regression suite replayed after a policy change with an automated diff.
- Regulatory mapping fully verified.
- Symantec design complete for 4 use cases with explicit "not tested" status.
