# Positioning

## Repository name

| Option | Assessment |
|---|---|
| `banking-dlp-controls-lab` | **Recommended.** Vendor-neutral (survives the Symantec phase), "controls" signals GRC and audit, "lab" sets an honest scope. |
| `purview-symantec-dlp-banking` | Search-friendly, but ties the name to two products and reads as a tool comparison rather than a control framework. |
| `ch-lu-bank-dlp-framework` | Precise on jurisdictions, but "framework" alone suggests a production methodology the repo does not claim. |

**GitHub description (short):** Reproducible DLP control framework for Swiss and Luxembourg banks. Microsoft Purview then Symantec DLP, synthetic data only.

**Topics:** `dlp`, `data-loss-prevention`, `microsoft-purview`, `symantec-dlp`, `data-security`, `banking`, `dora`, `gdpr`, `finma`, `cssf`, `grc`.

## Longer presentation

This repository turns banking data-protection risks into testable DLP controls. It starts from a regulatory and risk layer, defines vendor-independent control objectives and use cases, implements them in Microsoft Purview, then translates the same use cases to Symantec DLP. Every policy is validated with synthetic files produced by a seeded generator and every result is recorded with a file hash, so the same test can be replayed after each tuning change.

## Audience

- Hiring managers and technical interviewers for Data Security, DLP Engineering, DLP Governance and GRC roles.
- DLP practitioners in regulated financial institutions looking for a structured starting point.

## Objectives

| Business | Technical |
|---|---|
| Show how DLP maps to banking secrecy, professional secrecy, AML tipping-off, outsourcing and cross-border rules | Build and tune Purview policies across Exchange, SharePoint, OneDrive, Teams and Endpoint |
| Show a controlled rollout that does not break business flows | Produce a reproducible synthetic test corpus with checksum-valid identifiers |
| Show operating model: exceptions, triage, KPI/KRI, audit evidence | Automate evidence export and regression testing |
| Compare two DLP platforms on identical use cases | Keep a vendor-agnostic layer reusable across platforms |

## Scope

In scope: data classification, 15 banking use cases, Purview DLP (including Endpoint DLP, EDM, fingerprinting where the lab allows), Symantec DLP design, synthetic data, tests, governance, KPI/KRI, regulatory mapping for CH and LU.

Out of scope: production deployment claims, Insider Risk Management tuning beyond its interaction with DLP, CASB design, network architecture, email encryption design, any bypass or evasion content.

## Value

| For | Value |
|---|---|
| A Swiss bank | Treatment of client identifying data (CID) and banking secrecy as a detection and cross-border problem, not just a PII problem; FINMA critical data angle |
| A Luxembourg bank | DORA-aligned control evidence, professional secrecy and intra-group sharing, CSSF outsourcing constraints, employee monitoring prerequisites under Luxembourg labour law |
| A recruiter or interviewer | Traceable chain from regulation to tested policy, visible engineering (generator, CI, PowerShell), honest status labels |

## Disclaimer

Independent lab. Not affiliated with any financial institution, employer or client. Uses synthetic data exclusively. Nothing here is legal advice. All configurations and results must be validated in an authorised environment before production use.
