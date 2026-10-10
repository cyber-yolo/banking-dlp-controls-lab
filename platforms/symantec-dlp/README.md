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

## Policy design example

See `policy-design/SY-POL-001.yaml` (translation of PV-POL-001).

## Incident workflow (design)

`New` then `In triage` then either `False positive`, `Authorised activity`, `Escalated` (Compliance, Legal, HR, SOC) or `Confirmed violation`, then `Resolved`. Status values are custom attributes in Enforce; the same qualification codes as `operations/alert-triage-playbook.md` are used so KPIs are comparable across platforms.

## What cannot be claimed without a lab

- Detection accuracy on the synthetic corpus.
- Endpoint agent behaviour per browser and application.
- Response rule user experience (justification prompts).
- Performance and incident volume.
