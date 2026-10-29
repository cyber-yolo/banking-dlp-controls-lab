# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning: SemVer, pre-1.0 minor versions map to roadmap milestones.

## [Unreleased]

### Added

- Repository structure, security baseline, CI.
- Banking data taxonomy (5 levels) and data catalog (21 categories).
- Use case catalog (15 use cases) and 4 detailed use case sheets.
- Purview policy specifications PV-POL-001 to PV-POL-003, custom SIT rule package draft, lab PowerShell scripts.
- Synthetic data generator with seed, manifest, hashing, validators and unit tests.
- Test strategy, test matrix, 3 filled test cases.
- Regulatory mapping methodology and draft mapping (references to verify).
- Governance: lifecycle, RACI, triage playbook, exception management, KPI/KRI.
- Symantec DLP design and Purview vs Symantec matrix (design only).
- Purview lab campaign v0.3 on a trial tenant: 6 runs passed (SMOKE-001, TC-001, TC-002, TC-003a, TC-003b, TC-003c). Observed: IBAN detection at High confidence, R1/R2/R3 routing by count, docx attachment extraction, negative control, external delivery. Redacted evidence in `evidence-public/`, including a configuration export of PV-POL-001.
- Troubleshooting guide `docs/lab-troubleshooting/purview-dlp-email.md` (550 5.7.501, custom domain, reading Activity Explorer and message trace).
- `validate-repo` detects lab identifiers listed in a local, git-ignored `.lab-denylist`.
- Symantec DLP design v0.9 (#31): SY-POL-002 (endpoint egress, UC-003), SY-POL-003 (GenAI, UC-004), SY-POL-004 (Discover, UC-005), SY-POL-005 (AML tipping-off, UC-010); test cases TC-101 to TC-118, all design only / not tested; named gaps for Teams (UC-006) and scan-based SharePoint control (UC-005).
- Generator scenario SCN-014 (UC-010 false positive): AML training material with AML vocabulary and no client ID, used by TC-116. Existing scenario files and their hashes are unchanged.

### Changed

- `New-LabDlpPolicy.ps1`: alert recipient is an SMTP address (`-AlertRecipient`), the script stops when a rule fails to create, and thresholds use `confidencelevel`.
- Published evidence moved from `evidence/` to `evidence-public/`. `evidence/` stays git-ignored for raw files.
- Assumptions and limits updated (A-01, A-04, GAP-03, GAP-04 closed; GAP-05 and a `DistributionStatus` note added).
- TC-010, TC-011 and TC-012 closed as NOT RUN: the trial tenant was disabled on 25 October 2026. TC-004 to TC-009 remain NOT RUN (Endpoint DLP needs a Windows 11 VM).
- The block action is not validated: simulation mode does not enforce `BlockAccess`.
- README Status table, Purview README and `PV-POL-001.yaml` aligned with the v0.3 results: PV-POL-001 set to `lab-tested` (S1 simulation, block not validated), custom SIT rule package marked imported but not tested.
- Purview vs Symantec matrix: all 15 use cases listed, with policy IDs and separate Purview and Symantec test status. UC-012 and UC-014 Symantec coverage changed from "Partial (design)" to "Not designed", as no spec exists.

### Fixed

- Test matrix: added the missing SMOKE-001 evidence file and corrected its link.
