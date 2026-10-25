# Symantec DLP translation

Status: **design only, not tested.** No Symantec DLP licence or lab is assumed. Target version assumption: 16.x (Broadcom). Feature availability varies by version and licensed modules; every item below must be confirmed against the version actually used before any claim of coverage.

## Principle

Same use cases, same control objectives, same synthetic test files, same acceptance criteria as Purview. Where Symantec has no equivalent, the gap is documented. No forced equivalence.

## Component mapping

| Purview concept | Symantec DLP concept | Notes |
|---|---|---|
| Purview portal / policy engine | Enforce Server (console, policies, incidents) | Central management |
| Exchange Online DLP | Network Prevent for Email (MTA integration) or cloud email detection | Architecture choice: on-premises MTA hop vs cloud service |
| Endpoint DLP | Endpoint Prevent (agent) | USB, print, clipboard, browser, network share, application monitoring |
| SharePoint / OneDrive DLP | Network Discover (scan) and cloud detection options | Discovery scan vs inline control differ in timing |
| Web upload / GenAI domains | Network Prevent for Web (proxy integration) and Endpoint Prevent (browser) | Requires proxy (ICAP) for network path |
| Teams DLP | No native inline equivalent assumed | Documented as a gap (UC-006) |
| Sensitive Information Types | Data Identifiers (built-in and custom), keyword and regex rules | IBAN identifiers exist in regional variants; confirm which covers CH and LU |
| Exact Data Match | Exact Data Matching (EDM) | Profile built from a synthetic customer table |
| Document Fingerprinting | Indexed Document Matching (IDM) | KYC form template |
| Trainable classifiers | Vector Machine Learning (VML) | Evaluate only |
| Sensitivity labels | Detection of label metadata (for example Microsoft Information Protection labels) where supported | Confirm per version |
| Policy actions | Response rules (block, notify, user cancel with justification, redirect, modify message) | Smart response rules for analyst actions |
| Alerts, Activity Explorer | Incident reports, incident queues, status and severity attributes | Remediation workflow configured in Enforce |

## Policies

All specs are design only. None has been deployed or tested.

| Policy | Translates | Use cases | Components | Spec | Tests |
|---|---|---|---|---|---|
| SY-POL-001 External email, bank account data | PV-POL-001 | UC-001 | Network Prevent for Email | `policy-design/SY-POL-001.yaml` | TC-101 to TC-103 |
| SY-POL-002 Endpoint egress of restricted data | PV-POL-002 | UC-003 (primary), UC-002, 007, 008, 009 | Endpoint Prevent | `policy-design/SY-POL-002.yaml` | TC-104 to TC-107 |
| SY-POL-003 Generative AI | PV-POL-003 | UC-004 | Endpoint Prevent, Network Prevent for Web | `policy-design/SY-POL-003.yaml` | TC-108 to TC-113 |
| SY-POL-004 KYC files shared externally | PV-POL-004 (backlog) | UC-005 | Network Discover, Network Protect | `policy-design/SY-POL-004.yaml` | TC-117 |
| SY-POL-005 AML tipping-off | PV-POL-006 (backlog) | UC-010 | Network Prevent for Email, Endpoint Prevent (print) | `policy-design/SY-POL-005.yaml` | TC-114 to TC-116 |
| SY-POL-006 to 010 | | UC-011 to UC-015 | | not designed | |

Coverage, limits and test status per use case: `comparison/purview-vs-symantec.csv`. Test rows: `testing/test-matrix.csv` (platform `Symantec DLP`, status `N/A`).

## Named gaps

| Gap | Use case | Why | Consequence |
|---|---|---|---|
| Teams has no native inline control | UC-006, and the Teams channel of UC-010 | No Symantec inline inspection of Teams messages assumed for 16.x on-premises | PAN in Teams and tipping-off by chat are not covered on the Symantec side. TC-118 kept for traceability only |
| SharePoint/OneDrive control is scan-based | UC-005 | Network Discover finds the file at the next scan; Purview blocks at share time | Exposure window = scan interval + remediation time; TC-117 measures it. A cloud CASB would close it but is a separate product |
| No send-time justification on email | UC-001, UC-010 | Network Prevent for Email blocks or modifies; it has no equivalent of the Purview policy tip override | Block plus a documented release process |
| No native aggregation alert | UC-009 | No threshold alert equal to the Purview aggregation assumed | Saved report or SIEM correlation |
| Missing corpus scenario | UC-010 | No AML-without-client-ID file in `config.example.yaml` | TC-116 (and the UC-010 negative test on Purview) cannot run until it is added |

## Test data

Symantec tests reuse the Purview corpus file for file, so a future lab run compares like with like. Where a Purview run already recorded a SHA-256 (SCN-001, 002, 003, 004, 011 docx), the same hash is referenced; other files say `manifest`, to be filled from `output/manifest.json` of the run.

Note: regenerating `config.example.yaml` in a different environment gave different docx hashes from the ones recorded in the lab (library versions differ). Record the generator environment with the manifest, and check the hash of the file actually used before each run.

## Incident workflow (design)

`New` then `In triage` then either `False positive`, `Authorised activity`, `Escalated` (Compliance, Legal, HR, SOC) or `Confirmed violation`, then `Resolved`. Status values are custom attributes in Enforce; the same qualification codes as `operations/alert-triage-playbook.md` are used so KPIs are comparable across platforms.

## What cannot be claimed without a lab

- Detection accuracy on the synthetic corpus.
- Endpoint agent behaviour per browser and application.
- Response rule user experience (justification prompts).
- Performance and incident volume.
