# Microsoft Purview implementation

Status: designed, not lab-tested. Feature names and licensing must be re-checked against current Microsoft documentation during v0.3, as Purview evolves quickly.

## Architecture

| Layer | Purview capability | Used for |
|---|---|---|
| Classification | Built-in SITs: International banking account number (IBAN), Credit card number, SWIFT code, credential SITs, national ID SITs for CH/LU (verify availability) | DC-04, DC-05, DC-09, DC-19 |
| Classification | Custom SITs (`custom-sits/`): client ID, portfolio ID, AML vocabulary | DC-01, DC-03, DC-11 |
| Classification | Exact Data Match on a synthetic customer master | DC-01, DC-21 (UC-012) |
| Classification | Document fingerprinting on the synthetic KYC form template | DC-02 |
| Classification | Trainable classifiers (evaluate only) | DC-17 |
| Labelling | Sensitivity labels mapped to L0-L4 (`data-classification/taxonomy.yaml`) | All |
| Enforcement | DLP policies on Exchange, SharePoint, OneDrive, Teams, Endpoint | UC-001 to UC-015 |
| Enforcement | Endpoint DLP settings: removable storage groups, printer groups, service domain groups, restricted apps, network share groups | UC-002, 003, 004, 007, 008 |
| Detection and response | DLP alerts (Purview / Defender XDR), Activity Explorer, unified audit log | CO-08 |
| Governance | Role separation (admin vs analyst vs content viewer) | CO-08 |

## Licensing dependencies (to verify in lab)

| Capability | Typical requirement |
|---|---|
| DLP for Exchange, SharePoint, OneDrive | E3 or equivalent |
| DLP for Teams chat and channel messages | E5 / E5 Compliance / add-on |
| Endpoint DLP | E5 / E5 Compliance / add-on |
| Exact Data Match | E5 / E5 Compliance |
| Automatic labelling, advanced classification | E5 / E5 Compliance |

## Controlled rollout

| Stage | Purview mode | Scope | Exit criteria to next stage |
|---|---|---|---|
| S0 Design | none | Spec in `policies/` | Spec reviewed; tests defined; owner named |
| S1 Simulation | `TestWithoutNotifications` | All in-scope users | 2 weeks of events (lab: full regression set); sample of 50 matches reviewed; FP rate below 20% |
| S2 Simulation + tips | `TestWithNotifications` | All in-scope users | User feedback reviewed; tip text approved; FP rate below 10% |
| S3 Pilot enforcement | `Enable`, block with override | Pilot group | No business-blocking incident in 2 weeks; justification reasons analysed |
| S4 Block with justification | `Enable`, block with override | All in-scope users | Override rate stable and explained; exceptions registered |
| S5 Strict block | `Enable`, block without override | Targeted rules only (L4, high thresholds) | Owner and Compliance sign-off |

Rollback: every stage change is a PR referencing the evidence; reverting the mode is the documented rollback.

## Policies

| Policy | Use cases | Locations | Spec |
|---|---|---|---|
| PV-POL-001 External email, bank account data | UC-001 | Exchange | `policies/PV-POL-001.yaml` |
| PV-POL-002 Endpoint egress of restricted data | UC-002, 003, 007, 008, 009 | Endpoint | `policies/PV-POL-002.yaml` |
| PV-POL-003 Generative AI protection | UC-004 | Endpoint (browser), service domains | `policies/PV-POL-003.yaml` |
| PV-POL-004 to 011 | UC-005 to UC-015 | various | backlog |

## Scripts

| Script | Purpose | Safety |
|---|---|---|
| `scripts/New-LabDlpPolicy.ps1` | Create PV-POL-001 from parameters | Defaults to simulation; supports `-WhatIf` |
| `scripts/Export-DlpConfiguration.ps1` | Export policies, rules and custom SITs to JSON with SHA-256 for evidence and drift detection | Read-only; strips identifiers; output git-ignored |

## Endpoint DLP strategy

| Activity | Default for L3 | Default for L4 | Notes |
|---|---|---|---|
| Copy to removable USB | Block, approved device group audit | Block | Device groups by VID/PID or serial |
| Print | Block with override, approved printer group allowed | Block | Printer groups |
| Copy to clipboard / paste to browser | Audit (L3), block to GenAI domains | Block | Paste to browser requires supported browser |
| Upload to cloud service domains | Block with override outside sanctioned domains | Block | Service domain allow/block lists |
| Copy to network share | Audit, block outside approved shares | Block | Network share groups |
| Access by unallowed apps | Block | Block | Restricted apps list (sync clients, unsanctioned tools) |
