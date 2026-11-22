# Lab rebuild runbook (Purview, new trial tenant)

Status: procedure, not executed. Nothing in this file is a test result. A test stays `NOT RUN` in `testing/test-matrix.csv` until it is observed.

Purpose: rebuild the v0.3 Purview lab on a new trial tenant with the configuration already versioned in this repository, then add what is missing to run TC-004 to TC-009 (Endpoint DLP) and TC-010 to TC-012 (issue #22).

## 0. Conventions

| Item | Rule |
|---|---|
| Placeholders | `<tenant>` (tenant name), `<lab-domain>` (custom domain), `<admin-upn>`, `user1@<lab-domain>`, `user2@<lab-domain>`, `<external-recipient>` (personal mailbox outside the tenant). In committed evidence, use `external-recipient@redacted.example` and `user@redacted.example`. |
| Never committed | Tenant name, lab domain, any `*.onmicrosoft.com`, tenant ID, real mailbox addresses, Alert, Policy, Record and mailbox item IDs, unredacted screenshots. |
| Commands | PowerShell 7, one line per command (statements joined with `;`), run from the root of the local clone. |
| Source of truth | Each configuration value below points to its source file. Where the repository has no value, the step says **GAP** and the value must be decided and committed before the step is run. Gaps are listed in section 12. |
| Timestamps | Record every action in UTC. See section 5.6 for the message trace time zone pitfall. |

## 1. Before signup

1. Block time: the trial lasts about one month and evidence is lost when it ends (`docs/lab-troubleshooting/purview-dlp-email.md`, section 4). Plan sections 2 to 8 in the first week, tests in weeks 2 and 3, final export in week 3 (section 10).
2. Install PowerShell 7 (Windows PowerShell 5.1 fails with PackageManagement conflicts, `docs/03-lab-setup.md`): `winget install Microsoft.PowerShell`
3. Install the module: `Install-Module ExchangeOnlineManagement -Scope CurrentUser`
4. Rebuild the synthetic corpus (never committed) and check the hashes: `cd synthetic-data-generator; python -m dlpgen generate --config config.example.yaml; python -m dlpgen validate-output --manifest output/manifest.json; cd ..`
5. Check that the hashes of the reused files still match `testing/test-matrix.csv` (for example SCN-001-DOCX `212933cf...`, SCN-004-DOCX `2131fc52...`). A mismatch means the generator changed: stop and investigate.
6. Update the local, git-ignored `.lab-denylist` with the new tenant name, the lab domain and the external mailbox, one term per line after a `#` comment line. Run `cd synthetic-data-generator; python -m dlpgen validate-repo --root ..; cd ..`. Expected: `validate-repo: OK`.

## 2. Tenant

### 2.1 Licence choice

| Need | Licence (per Microsoft licensing guidance, re-check at signup) |
|---|---|
| DLP for Exchange (PV-POL-001, TC-010 to TC-012) | Office 365 E5 or Microsoft 365 E5 |
| Endpoint DLP (PV-POL-002, PV-POL-003, TC-004 to TC-009) | Microsoft 365 E5, or an E3 base plus the Microsoft 365 E5 Compliance add-on (now sold as Microsoft Purview Suite) or E5 Information Protection and Governance |

The v0.3 tenant used an **Office 365 E5** trial (`docs/03-lab-setup.md`). Office 365 E5 is not listed by Microsoft as a licence for Endpoint DLP, so the same SKU is not enough for this rebuild. Pick a **Microsoft 365 E5** trial. If only a business or E3 trial can be created at signup, add a Purview / E5 Compliance trial from the admin center (Billing > Purchase services) before section 7.

The Microsoft Learn device onboarding pages do not name the SKU; they link to the service descriptions. Record the licence actually used in `docs/03-lab-setup.md` (section "As built").

### 2.2 Signup

1. Sign up for the trial with a payment method. Choose `<tenant>`: it is permanent and must not contain a personal name.
2. Enable MFA on the first admin account (Global Administrator).
3. Write down, outside the repository: trial start date, trial end date and auto-renew date shown in Billing > Your products. Set a reminder to cancel at least 3 days before renewal (v0.3: created 11 October, cancel before 10 November).

Check: admin center opens, Billing shows the trial as Active.

## 3. Custom domain

The domain was removed from the old tenant several weeks ago and is reusable.

1. Admin center > Settings > Domains > Add domain > `<lab-domain>`. If the wizard says the domain is already in use, the old tenant still holds it: stop, do not try to force it.
2. Add the TXT verification record at the DNS provider, then Verify.
3. Add the records the wizard asks for: MX, SPF (TXT), autodiscover CNAME. If the DNS provider proxies records, keep mail records on DNS only (`purview-dlp-email.md`, section 2).
4. Keep WHOIS privacy on at the registrar.
5. Set `<lab-domain>` as the default domain, so new users get it as primary address.

Check: domain status is Healthy in the admin center. `Resolve-DnsName -Type MX <lab-domain>` returns the Microsoft 365 MX.

## 4. Audit and admin roles

Do this right after signup: audit ingestion and role changes take time.

1. Connect: `Connect-ExchangeOnline -UserPrincipalName <admin-upn>`
2. Check audit: `Get-AdminAuditLogConfig | Format-List UnifiedAuditLogIngestionEnabled`. Expected: `True`. If not: `Enable-OrganizationCustomization; Set-AdminAuditLogConfig -UnifiedAuditLogIngestionEnabled $true`
3. Add the admin to *Organization Management* (Global Administrator alone did not give audit search in v0.3, `docs/lab-troubleshooting/purview-audit.md`): `Add-RoleGroupMember "Organization Management" -Member "<admin-upn>"; Get-RoleGroupMember "Organization Management"`
4. Disconnect, reconnect, wait up to one hour before concluding that audit search fails. Audit events take 60 to 90 minutes to appear.

Check, the next day: `Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-1) -EndDate (Get-Date) -ResultSize 5` returns records.

## 5. Purview configuration (as versioned)

Connect: `Connect-IPPSSession -UserPrincipalName <admin-upn>`

### 5.1 Custom SIT rule package

Source: `platforms/microsoft-purview/custom-sits/banking-lab-sit-rulepack.xml`

| SIT | Pattern | Confidence | Keywords | Proximity |
|---|---|---|---|---|
| Custom - Client ID (CLT) | `\bCLT-\d{8}\b` | 85 with `Keyword_client_context`, 65 without | client, client ID, numero client, Kundennummer, relationship manager | 300 |
| Custom - Portfolio ID (PF) | `\bPF-\d{2}-\d{6}\b` | 75 with `Keyword_portfolio_context` | portfolio, portefeuille, Depot, holdings, valuation | 300 |
| Custom - AML vocabulary with client ID | `Regex_client_id` + `Keyword_aml_vocabulary` | 85 | suspicious activity report, suspicious transaction report, SAR, STR, declaration de soupcon, CRF, MROS, Verdachtsmeldung, money laundering, blanchiment | 300 |

1. Import: `New-DlpSensitiveInformationTypeRulePackage -FileData ([System.IO.File]::ReadAllBytes((Resolve-Path ".\platforms\microsoft-purview\custom-sits\banking-lab-sit-rulepack.xml")))`
2. If the import fails on encoding, re-save the file as Unicode (UTF-16) in a local copy, not in git (comment in the XML file).
3. Check: `Get-DlpSensitiveInformationType | Where-Object Publisher -eq "banking-dlp-controls-lab" | Format-Table Name`. Expected: the three names above.
4. Test the SITs (roadmap 0.3 acceptance criterion, never evidenced in v0.3): `Test-DataClassification -TextToClassify "Client ID CLT-12345678 relationship manager" | Select-Object -ExpandProperty ClassificationResults`. Expected: Client ID (CLT) at confidence 85. Repeat without the keywords (expected 65) and with an AML term near the ID (expected AML SIT). Save the output in `evidence/` (raw, git-ignored).

The XML header still says "NOT imported" while the README says "imported, not tested". Update the header after this step.

### 5.2 Sensitivity labels

Source: `data-classification/taxonomy.yaml` and GAP-05 in `docs/02-assumptions-and-limits.md`.

v0.3 did **not** create the taxonomy labels. The tenant only had the default labels, and `General\All Employees (unrestricted)` was applied to every test message and attachment. Rebuilding "as is" means: no custom label.

| Level | Target Purview label (taxonomy) |
|---|---|
| L0 | Public |
| L1 | General |
| L2 | Confidential |
| L3 | Highly Confidential - Restricted |
| L4 | Highly Confidential - Secret |

**GAP**: PV-POL-002 and PV-POL-003 use `label_in: [L3, L4]` as a detection path, but no label publishing policy, default label or auto-labelling setting is specified. TC-004 to TC-009 can run on SIT detection only. Decide before section 8 whether to create the L3/L4 labels (and how they are applied) or keep GAP-05 open.

Pitfall: a default label may still be applied to test files. It did not change file bytes in v0.3 (SHA-256 checked), so check the hash of every received or copied file again.

### 5.3 PV-POL-001 and rules R1, R2, R3

Sources: `platforms/microsoft-purview/policies/PV-POL-001.yaml`, `platforms/microsoft-purview/scripts/New-LabDlpPolicy.ps1`, export `evidence-public/config-export/20261020T223542Z/`.

| Item | Value |
|---|---|
| Policy name | `PV-POL-001 External email - bank account data` |
| Location | Exchange, All |
| Mode | `TestWithoutNotifications` (S1 simulation) |
| Comment | `banking-dlp-controls-lab \| UC-001 \| spec policies/PV-POL-001.yaml` |
| SIT | International banking account number (IBAN), `confidencelevel High` (min 85) |
| Scope | `AccessScope NotInOrganization` |
| Policy tip text | `LAB: this message contains client account data. External sending of client data is restricted. See the data handling guideline.` |

| Rule | IBAN count | Action | Severity | Alert mail | NotifyUser |
|---|---|---|---|---|---|
| `PV-POL-001-R1 Low volume notify` | 1 to 4 | audit, policy tip | Low | none (`GenerateAlert` empty) | LastModifier |
| `PV-POL-001-R2 Block with justification` | 5 to 19 | `BlockAccess`, `NotifyAllowOverride WithJustification` | Medium | yes, to `-AlertRecipient` | LastModifier |
| `PV-POL-001-R3 Strict block` | 20 or more | `BlockAccess` | High | yes, to `-AlertRecipient` | LastModifier |

1. Dry run: `.\platforms\microsoft-purview\scripts\New-LabDlpPolicy.ps1 -AlertRecipient <admin-upn> -WhatIf`
2. Create: `.\platforms\microsoft-purview\scripts\New-LabDlpPolicy.ps1 -AlertRecipient <admin-upn>`. Defaults are `-Mode TestWithoutNotifications -BlockThreshold 5 -StrictThreshold 20`. The script has been corrected since v0.3 and never re-run: watch for errors on the first rule.
3. Check: `Get-DlpComplianceRule -Policy "PV-POL-001 External email - bank account data" | Format-Table Name,ReportSeverityLevel,BlockAccess,NotifyAllowOverride,GenerateAlert`
4. Exception "recipient_domain_in, approved correspondent domains" in the spec is not implemented by the script and was not in v0.3. Leave it out (same as v0.3).

Pitfalls:

- `DistributionStatus` may stay `Pending` while `DistributionSyncStatus` is `Success`. Judge distribution by behaviour (section 6), not by that field (`docs/02-assumptions-and-limits.md`).
- Simulation mode does not enforce `BlockAccess`. A block rule still delivers the message. See the decision in section 12 (G-01) before running tests that expect a block.

### 5.4 Alerts

| Item | Value | Source |
|---|---|---|
| Alerting rules | R2 and R3 only | `New-LabDlpPolicy.ps1` |
| Recipient | the admin mailbox (`user@redacted.example` in the export) | `rules.json` in the 2026-10-20 export |
| Alert view | Purview > Data loss prevention > Alerts, and the alert mail | evidence `SMOKE-001`, `TC-001`, `TC-003c` |

No R1 mail is expected. Its absence is not a failure.

### 5.5 Baseline export

Right after 5.3: `.\platforms\microsoft-purview\scripts\Export-DlpConfiguration.ps1`. Output goes to `evidence/config-export/<UTC timestamp>/` (git-ignored). Compare with `evidence-public/config-export/20261020T223542Z/` (rules, thresholds, severities, mode). Differences are drift and must be explained before testing.

The 2026-10-20 manifest lists `custom-sits.json`, but that file is not in `evidence-public/`. Publish a redacted copy this time if it contains no identifier.

### 5.6 Reading results (pitfalls from v0.3)

From `docs/lab-troubleshooting/purview-dlp-email.md`, section 3:

- Activity Explorer: set the filter set to **None**. The predefined set "DLP policy rules that detected activities" hid the events. Read the matched rule in the event detail. The IBAN count is not shown, nor in the CSV export: for R1 only the band can be recorded.
- Message trace: the portal labelled times UTC+01:00 but showed Paris local time. Since 25 October 2026 Paris is UTC+01:00 again, so both match until 29 March 2027, then differ by one hour. Always convert to UTC before comparing with alerts.
- Audit search: do not start a second unfiltered search while one is Queued.

## 6. Accounts and mailboxes

Source: `docs/03-lab-setup.md`. v0.3 planned 4 users. This rebuild uses 1 admin and 2 users.

| Account | Role in tests | Licence | Admin roles |
|---|---|---|---|
| `<admin-upn>` | DLP admin, alert recipient | Microsoft 365 E5 (needs a mailbox for alert mails) | Global Administrator, *Organization Management* (section 4) |
| `user1@<lab-domain>` | Sender for Exchange tests, signed-in user on the Windows 11 VM | Microsoft 365 E5 | none |
| `user2@<lab-domain>` | Internal recipient (UC-010 "internal outside compliance"), non-pilot user | Microsoft 365 E5 | none |

Use names from the synthetic generator, never real names.

1. Admin center > Users > Active users > Add a user, for user1 and user2. Primary address on `<lab-domain>`, usage location set, licence assigned.
2. Wait for the mailboxes (up to about 1 hour). Check: `Get-Mailbox | Format-Table DisplayName,PrimarySmtpAddress,RecipientTypeDetails`
3. Sign in to Outlook on the web as user1 and send one plain message to `<external-recipient>`.

Segregation (`docs/03-lab-setup.md`): Activity Explorer and Content Explorer viewing roles should go to an analyst account, not the admin. With 2 users only, this is not reproduced. Record it as a limit.

### 6.1 External delivery and 550 5.7.501

If the external message is rejected with `550 5.7.501` (`purview-dlp-email.md`, section 1):

1. Read the exact error in the message trace before changing anything.
2. Check that the sender address is on `<lab-domain>`, not on the `onmicrosoft.com` domain.
3. If it still fails, open a support request with the trace details. Do not retry in a loop.

Do not record the custom domain as the cause of a fix: v0.3 never isolated it.

## 7. Rebuild regression (before any new test)

Goal: prove that the rebuilt tenant behaves like the v0.3 tenant before using it for new tests. Allow for policy distribution first (v0.3: the policy worked the same evening).

| Run | File | Expected | v0.3 reference |
|---|---|---|---|
| SMOKE-002 | 5 synthetic IBANs typed in the body, user1 to `<external-recipient>` | R2, Medium, alert mail | `evidence-public/test-runs/SMOKE-001/` |
| TC-003b rerun | SCN-003-DOCX (5 IBAN CH) | R2, Medium, alert mail | `evidence-public/test-runs/TC-003b/` |

If both match, the rebuild is equivalent for PV-POL-001. Record them as new runs with their own date, never by editing the v0.3 rows. TC-003b also still lacks its Activity Explorer screenshot (`evidence-public/README.md`): capture it this time.

## 8. Windows 11 VM and Endpoint DLP onboarding

Sources: `docs/03-lab-setup.md`, `docs/02-assumptions-and-limits.md` (A-02). Prerequisites below are from Microsoft Learn "Get started with endpoint data loss prevention" and "Onboard Windows devices into Microsoft 365 overview", read in November 2026. Re-check before use.

### 8.1 VM

| Requirement | Value |
|---|---|
| OS | Windows 11 x64, 22H2 or later, Pro or Enterprise (Home cannot join Entra ID). The Windows 11 Enterprise evaluation image works for a lab. |
| Join state | Microsoft Entra joined (signed in as user1). Workgroup only is not supported. |
| Hypervisor | Must provide TPM 2.0 and Secure Boot, and **USB passthrough** of a physical USB stick for TC-004 and TC-005. A disk attached as a virtual hard disk appears as a fixed disk, not as removable storage. To verify on the chosen hypervisor before starting. |
| USB stick | One physical stick, with VID, PID and serial noted (Device Manager > Details > Hardware Ids). Used for TC-004 (not approved) then TC-005 (approved group). |
| Printer | Microsoft Print to PDF (built in), for TC-006 |
| Browser | Microsoft Edge (native Endpoint DLP support). Chrome or Firefox need the Microsoft Purview extension. |

### 8.2 Device prerequisites

1. Windows Update fully applied.
2. Defender antivirus: Anti-malware client version 4.18.2110 or newer, real-time protection and behaviour monitoring on. Check: `Get-MpComputerStatus | Select-Object AMProductVersion,RealTimeProtectionEnabled,BehaviorMonitorEnabled`
3. Microsoft 365 Apps 16.0.14701.0 or later, if Office files are opened on the VM.
4. Join: Settings > Accounts > Access work or school > Connect > Join this device to Microsoft Entra ID, with user1. Check: `dsregcmd /status` shows `AzureAdJoined : YES`.

### 8.3 Onboarding (local script)

The local script is meant for up to 10 devices, which fits this lab.

1. Purview portal > Settings > Device onboarding > Devices > Turn on device onboarding. Required role: Compliance admin, Security admin or Global admin (Entra roles, not Purview roles). It usually takes about a minute, up to 30 minutes.
2. Onboarding > Local script > download `DeviceComplianceOnboardingPackage.zip`. Keep it out of the repository: it identifies the tenant.
3. On the VM, from an elevated prompt: `DeviceComplianceLocalOnboardingScript.cmd`
4. Check: the device appears in Settings > Device onboarding > Devices with a healthy configuration status. Allow up to 30 minutes. Record the time.

## 9. Endpoint configuration

### 9.1 Endpoint DLP settings

Source: `platforms/microsoft-purview/policies/PV-POL-002.yaml` (`endpoint_settings_required`), `PV-POL-003.yaml`. Path: Purview > Data loss prevention > Overview > Data loss prevention settings > Endpoint settings.

| Setting | Group name (spec) | Content | Used by |
|---|---|---|---|
| Removable USB device groups | Approved encrypted USB | VID/PID or serial of the lab stick (8.1). Add it only before TC-005. | TC-005 |
| Printer groups | Approved secure print | **GAP**: no printer named. Not needed for TC-006, which uses a non-approved printer. | none |
| Sensitive service domain groups | Sanctioned cloud storage | **GAP**: no domain listed | TC-007 (control) |
| Sensitive service domain groups | Personal webmail | **GAP**: no domain listed | UC-002 (no TC) |
| Sensitive service domain groups | Non-sanctioned cloud storage | **GAP**: no domain listed | TC-007 |
| Sensitive service domain groups | Non-sanctioned GenAI | **GAP**: no domain listed | TC-008, TC-009 |
| Restricted apps | Unsanctioned sync clients | **GAP**: no app listed | no TC |

Commit the chosen domains in the policy specs before running the tests.

### 9.2 PV-POL-002 Endpoint egress (portal, no script)

Source: `platforms/microsoft-purview/policies/PV-POL-002.yaml`. No script exists for endpoint policies: create in the portal, then export (5.5).

| Item | Value |
|---|---|
| Name | `PV-POL-002 Endpoint egress - restricted data` |
| Location | Devices, all onboarded devices, all users |
| Detection (any of) | IBAN min count 5; Custom - Client ID (CLT) min count 1, confidence 85; label L3 or L4 (**GAP**, 5.2); fingerprint "Synthetic KYC form v1" (**GAP**: no fingerprint defined in the repo) |
| Copy to removable USB | block; approved group: audit |
| Print | block with override; approved group: audit |
| Upload to cloud domain | sanctioned: audit; personal webmail: block with override; non-sanctioned: block with override |
| Copy to network share | audit |
| Access by restricted apps | block |
| Paste to browser | audit |
| User notification | endpoint notification with guideline link (**GAP**: no link or text in the spec) |
| Alerts | block events Medium; L4 events High; alert when 10 or more matching events by one user in 1 hour |
| Mode | `TestWithoutNotifications` (spec stage S0). See G-01. |

### 9.3 PV-POL-003 Generative AI (portal)

Source: `platforms/microsoft-purview/policies/PV-POL-003.yaml`. Activities for all rules: paste to browser and upload to cloud domain, restricted to the "Non-sanctioned GenAI" group.

| Rule | Detection | Action | Severity |
|---|---|---|---|
| `PV-POL-003-R1 L4 and credentials strict block` | label L4, credential SITs, Custom - AML vocabulary with client ID | block | High |
| `PV-POL-003-R2 L3 block with justification` | label L3, Custom - Client ID (CLT) high confidence, fingerprint Synthetic KYC form v1 | block with override | Medium |
| `PV-POL-003-R3 Visibility` | any SIT match | audit | Low |

**GAP**: "credential SITs" and "any SIT match" are not lists Purview accepts. For TC-009, R3 must at least include Custom - Client ID (CLT) at low confidence (65), otherwise SCN-006 cannot match. Decide and commit the SIT lists first.

### 9.4 Sync delay

Purview policy distribution and endpoint sync introduce delays (`docs/02-assumptions-and-limits.md`). Record the time each policy is saved and do not start TC-004 to TC-009 until at least one hour later. A negative result inside that window is inconclusive, not a FAIL.

## 10. Tests to run

Rows come from `testing/test-matrix.csv`. Only TC-001 to TC-003 have a test case file; write `testing/test-cases/TC-004.yaml` to `TC-012.yaml` (from `templates/test-case.yaml`) before running them. Expected results below are the matrix values, unchanged.

| Test | Policy | Channel | File | Expected | Prerequisite |
|---|---|---|---|---|---|
| TC-004 | PV-POL-002 | Copy to USB | SCN-001-DOCX (10 IBAN LU) | block | 8, 9.2 |
| TC-005 | PV-POL-002 | Copy to USB, approved group | SCN-001-DOCX | audit | stick added to "Approved encrypted USB" after TC-004 |
| TC-006 | PV-POL-002 | Print (Microsoft Print to PDF) | SCN-013-PDF (client ID + portfolio ID) | block with justification | 9.2 |
| TC-007 | PV-POL-002 | Edge upload to a non-sanctioned cloud domain | SCN-009-XLSX (KYC + IBAN) | block with justification | 9.1 domains |
| TC-008 | PV-POL-003 | Paste to browser, GenAI | SCN-007-TXT (client ID with context) | block with justification | 9.1, 9.3 |
| TC-009 | PV-POL-003 | Paste to browser, GenAI | SCN-006-TXT (client ID without context) | audit | 9.3 R3 gap closed |
| TC-010 | PV-POL-001 | Exchange external | SCN-005-DOCX (10 invalid IBAN) | none (false positive test) | 5.3 |
| TC-011 | PV-POL-001 | Exchange external | SCN-001-PNG (IBAN in image) | none (no OCR, known false negative) | 5.3 |
| TC-012 | PV-POL-006 | Exchange external | SCN-010-DOCX (AML + client ID) | block | **GAP**: PV-POL-006 has no Purview spec |

Notes per test:

- TC-004 to TC-007: SCN-009 and SCN-013 contain client IDs (generator `records.py`), so detection goes through Custom - Client ID (CLT) or IBAN count. Read the matched condition in Activity Explorer.
- TC-005: same file and stick as TC-004, only the device group changes.
- TC-007: use Edge. The service domain restriction only applies to uploads through Edge or a browser with the Purview extension.
- TC-012: PV-POL-001 covers IBAN only. Write `platforms/microsoft-purview/policies/PV-POL-006.yaml` from `use-cases/UC-010.yaml` (strict block external, 1 occurrence, Critical, restricted alert visibility) and align it with `platforms/symantec-dlp/policy-design/SY-POL-005.yaml`, then create it. Running SCN-014 as a negative control would also give a Purview mirror of TC-116.
- For each run: send or copy one file at a time, write the UTC time, keep the file SHA-256, check Activity Explorer (filter set None), alert, and message trace for Exchange tests.

## 11. Evidence export and redaction (before the trial ends)

When the subscription is disabled, mailbox access returns `TenantAccessBlockedException` and compliance cmdlets disappear. Anything not exported is lost (`purview-dlp-email.md`, section 4).

### 11.1 Export checkpoints

| When | Export |
|---|---|
| After 5.5 and after any policy change | `Export-DlpConfiguration.ps1` (PV-POL-001, then PV-POL-002, PV-POL-003, PV-POL-006) |
| After each test | Activity Explorer CSV and detail screenshots, alert mail, message trace (Exchange), endpoint notification screenshot (VM) |
| End of week 3, at the latest 7 days before the trial end date | Full export again, Endpoint DLP settings screenshots (device groups, domain groups), device list, audit search export for the test window |

Raw files go to `evidence/<TC-ID>/<timestamp>/` (git-ignored), with a SHA-256 for each file (`docs/03-lab-setup.md`).

### 11.2 Redaction before commit

Mask with opaque boxes, then strip PNG metadata (`evidence-public/README.md`):

- [ ] lab domain, tenant name, any `onmicrosoft.com` value
- [ ] Gmail local part and any real mailbox address
- [ ] tenant ID, including the URL shown in the browser status bar when hovering a link
- [ ] Alert IDs, Policy IDs, Record IDs, mailbox item IDs
- [ ] device name and device ID of the VM
- [ ] user, sender and recipient fields that show the lab domain

Then: update `.lab-denylist`, run `python -m dlpgen validate-repo --root ..`, and publish only redacted extracts under `evidence-public/test-runs/<run>/` (never `docs/evidence/`: any `evidence/` folder is ignored). Index each screenshot in `evidence-public/README.md`.

### 11.3 End of trial

1. Cancel the trial before the auto-renew date (2.2).
2. Mark untested items `NOT RUN` with the reason, as in v0.3.
3. Update `docs/03-lab-setup.md` (As built), `docs/02-assumptions-and-limits.md` and `CHANGELOG.md`.

## 12. Gaps and decisions before running

| ID | Gap | Where | Needed for |
|---|---|---|---|
| G-01 | All specs are in simulation (`TestWithoutNotifications`), which does not enforce `BlockAccess`. TC-004, TC-006, TC-007, TC-008 and TC-012 expect a block. Decide whether the lab moves these policies to `Enable` (S3) to observe the block, or records detection only, as in v0.3. | PV-POL-001/002/003 `deployment` | Every block test |
| G-02 | No L0 to L4 labels created, no labelling method specified (GAP-05) | 5.2 | Label detection paths of PV-POL-002/003 |
| G-03 | Fingerprint "Synthetic KYC form v1" not defined | 9.2, 9.3 | Optional for TC-007 |
| G-04 | Service domain groups, restricted apps and approved printers have no values | 9.1 | TC-007, TC-008, TC-009 |
| G-05 | PV-POL-003 "credential SITs" and "any SIT match" not mapped to SIT names | 9.3 | TC-009 |
| G-06 | No endpoint notification text or guideline link | 9.2 | User notification |
| G-07 | PV-POL-006 has no Purview spec | 10 | TC-012 |
| G-08 | No test case files TC-004 to TC-012 | 10 | All new tests |
| G-09 | `custom-sits.json` listed in the 2026-10-20 manifest but not published | 5.5 | SIT evidence |
| G-10 | Licence for Endpoint DLP to confirm at signup (Office 365 E5 is not enough per Microsoft licensing guidance) | 2.1 | Section 8 onward |
| G-11 | USB passthrough on the chosen hypervisor not verified | 8.1 | TC-004, TC-005 |
