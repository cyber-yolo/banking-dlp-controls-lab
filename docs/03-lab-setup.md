# Lab setup

Status: to be completed with actual lab details (redacted) during v0.3.

## Microsoft Purview lab

| Component | Purpose | Notes |
|---|---|---|
| Lab tenant | Policies, SITs, labels, alerts | Microsoft 365 E5 trial or equivalent. Check current trial and developer sandbox eligibility, which Microsoft has restricted over time. Never use an employer tenant. |
| 4 test users | Sender, pilot group member, non-pilot member, DLP analyst | Names from the synthetic generator; `.onmicrosoft.com` domain never committed |
| 1 external mailbox | External recipient for UC-001, UC-010, UC-011 | Personal throwaway mailbox, not committed |
| 1 SharePoint site + 1 Teams team | UC-005, UC-006 | Guest access enabled for external sharing tests |
| 1 to 2 Windows 11 VMs | Endpoint DLP (UC-002, UC-003, UC-004, UC-007, UC-008) | Onboard with the local script method, intended for a small number of test devices |
| Virtual USB device | UC-003 | USB passthrough or virtual removable media |
| Virtual printer (PDF) | UC-007 | Microsoft Print to PDF |

Roles: separate the DLP administrator account from the analyst account. Assign content viewing roles (Content Explorer, Activity Explorer) only to the analyst, to mirror a bank's segregation of duties.

## PowerShell

```powershell
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Connect-IPPSSession -UserPrincipalName <lab-admin-upn>
```

Scripts in `platforms/microsoft-purview/scripts/` default to simulation mode and support `-WhatIf`.

## Evidence handling

1. Store raw evidence locally in `evidence/<TC-ID>/<timestamp>/` (git-ignored).
2. Record the SHA-256 of each evidence file in the test matrix.
3. Commit only redacted extracts: tenant name, domain, user principal names, device names and GUIDs removed.

## Symantec DLP

No lab assumed. If access becomes available (training environment, vendor demo), record version, components and constraints here before any test.
