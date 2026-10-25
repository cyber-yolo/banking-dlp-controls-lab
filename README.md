# banking-dlp-controls-lab

> **Independent lab. Synthetic data only.** Not affiliated with any bank, financial institution, employer or client. Every identity, account, transaction and document in this repository is fictitious and marked `SYNTHETIC TEST DATA`. Configurations and results must be validated in an authorised environment before any production use.

A reproducible Data Loss Prevention (DLP) control framework for Swiss and Luxembourg banks, implemented first on **Microsoft Purview**, then translated to **Symantec DLP**, on top of a vendor-agnostic control layer.

## Executive summary

Banks do not fail at DLP because of missing licences. They fail on the chain between a regulatory expectation and a tuned, evidenced, operated policy. This repository makes that chain explicit and testable:

```text
Regulatory text -> Banking risk -> Control objective -> Use case -> Vendor policy -> Test case -> Synthetic test file -> Evidence -> KPI/KRI
     (RM-xx)                        (CO-xx)            (UC-xxx)   (PV-/SY-POL-xxx)  (TC-xxx)       (SCN-xxx)          (hash)    (KPI-xx)
```

What is in it:

| Layer | Content | Folder |
|---|---|---|
| Governance and risk | Taxonomy, data catalog, regulatory mapping (DORA, GDPR, nLPD, FINMA, CSSF, EBA, NIS2), RACI, exception management | `data-classification/`, `regulatory-mapping/`, `operations/` |
| Vendor-agnostic controls | 15 banking use cases, 8 control objectives, test strategy | `use-cases/`, `docs/01-architecture.md`, `testing/` |
| Engineering | Purview policy specs, custom SIT rule package, PowerShell lab scripts; Symantec DLP policy design | `platforms/` |
| Validation | Python generator of synthetic banking files (IBAN CH/LU with valid checksums, test PANs, KYC, AML, secrets) with seed, manifest and hashes | `synthetic-data-generator/` |
| Operations | Policy lifecycle, triage playbook, KPI/KRI | `operations/`, `dashboards/` |
| Repository security | CI (lint, tests, repo data validator, gitleaks), PR checklist, SECURITY.md | `.github/` |

## Status

Every artefact carries an explicit status. Nothing is claimed as tested until evidence exists.

| Area | Status |
|---|---|
| Taxonomy, catalog, use cases | Draft v0.2 |
| Purview PV-POL-001 (external email, IBAN) | **Lab-tested in simulation** (S1, v0.3). SMOKE-001, TC-001, TC-002, TC-003a, TC-003b, TC-003c PASS: IBAN detection at High confidence, R1/R2/R3 routing by count, docx attachment extraction, negative control. **Block action not validated**: simulation mode does not enforce `BlockAccess`. Evidence in [`evidence-public/`](evidence-public/), results in [`testing/test-matrix.csv`](testing/test-matrix.csv) |
| Purview PV-POL-002, PV-POL-003 (endpoint, generative AI) | Designed, **not lab-tested**. TC-004 to TC-009 NOT RUN (Endpoint DLP needs a Windows 11 VM and a lab tenant) |
| Purview custom SIT rule package | Imported in the v0.3 lab tenant, **not tested**: no policy used it, TC-012 NOT RUN |
| Purview lab tenant | v0.3 trial tenant disabled on 25 October 2026. TC-010 to TC-012 NOT RUN; any re-run needs a new tenant |
| Synthetic data generator | Working, unit-tested |
| Symantec DLP | Design only (no lab licence assumed) |
| Regulatory mapping | Draft, **all references TO VERIFY** against official texts |

## Quick start (synthetic data generator)

Requires Python 3.10 or later (3.12 matches CI).

### Linux / macOS

```bash
cd synthetic-data-generator
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m dlpgen generate --config config.example.yaml
python -m dlpgen validate-output --manifest output/manifest.json
python -m pytest -q
```

### Windows (PowerShell)

```powershell
cd synthetic-data-generator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m dlpgen generate --config config.example.yaml
python -m dlpgen validate-output --manifest output/manifest.json
python -m pytest -q
```

If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first, then activate again.

Generated files land in `synthetic-data-generator/output/`, which is git-ignored. Only configuration, seeds and code are versioned: the corpus is rebuilt on demand.

## Repository map

See [`docs/01-architecture.md`](docs/01-architecture.md) for the full tree and the purpose of each folder, and [`docs/05-roadmap.md`](docs/05-roadmap.md) for versions 0.1 to 1.0.

## Non-negotiable rules

1. No real customer, employee, account or document data. Ever.
2. No secrets, tokens, tenant identifiers, internal URLs or client names.
3. No screenshots of any environment other than a personal lab tenant, and those are redacted.
4. No content explaining how to bypass or disable security controls.
5. Regulatory references are separated from control recommendations; a DLP setting is never presented as a direct legal obligation unless the text says so.

## Licence

Code: MIT. Documentation: CC BY 4.0. See [`LICENSE`](LICENSE).
