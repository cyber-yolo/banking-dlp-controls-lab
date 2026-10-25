# Assumptions and limits

| ID | Assumption | Consequence if wrong |
|---|---|---|
| A-01 | A personal Microsoft 365 lab tenant with E5 or E5 Compliance capabilities is available (trial or sandbox) | Endpoint DLP, Teams DLP and EDM tests move to "design only". Trial tenant used for v0.3, disabled on 25 October 2026. |
| A-02 | One or two Windows 11 VMs can be onboarded to Endpoint DLP | Endpoint use cases (UC-003, UC-007, UC-008) remain untested |
| A-03 | No Symantec DLP licence or lab is available; target version assumed 16.x (Broadcom) | Phase 2 is a documented design, labelled "not tested" |
| A-04 | ~~An external mailbox outside the lab tenant is available as test recipient~~ | Invalidated on 15 October 2026: external delivery to a Gmail mailbox succeeded (see GAP-04). |
| A-05 | Repository language is English; French summaries may be added | None |
| A-06 | The lab tenant trial stays active for the full duration of v0.3 (1 month from 11 October 2026; cancel before 10 November 2026) | If the trial ends before evidence is collected, the tenant and its evidence are lost. Re-run on a new tenant and document the gap |

## What this repository does not prove

- Performance at production scale (volumes, latency, endpoint impact).
- Behaviour on a real bank's data, where false positive profiles are very different.
- Integration with a real SOC, ticketing or case management tool.

## Publication boundaries

| Content | Public repo | Lab tenant only | Never exported from a real environment |
|---|---|---|---|
| Policy intent, conditions, thresholds (spec) | Yes | | |
| Custom SIT regex and keywords (synthetic formats) | Yes | | |
| PowerShell scripts without identifiers | Yes | | |
| Policy exports from the lab | Sanitised extracts only | Full export | |
| Activity Explorer and alert screenshots | Redacted | Raw | |
| EDM schema (synthetic) | Yes | Hashed upload | |
| Any configuration, export, screenshot, alert or content from an employer or client | | | **Always excluded** |

## Known technical limits

- Purview and Symantec IBAN detection validate the ISO 7064 mod 97 checksum. Positive tests therefore use checksum-valid synthetic IBANs (see `synthetic-data-generator/README.md`). Invalid checksums are used only for false-positive tests.
- No official test range exists for IBANs. Synthetic IBANs use a zero bank code and the literal `SYNTH` in the account part to make collision with a real account practically impossible; residual risk is documented, not eliminated.
- Swiss AHV/AVS numbers and Luxembourg national identification numbers are **not generated** in v0.x: any checksum-valid value could belong to a real person. Detection of these types is documented but not tested.
- Purview policy distribution and endpoint sync introduce delays; tests record timestamps and allow for propagation before concluding.
- Audit search cmdlets and the portal search need the admin account in *Organization Management* in this setup. Audit events take 60 to 90 minutes to appear after activity. See `lab-troubleshooting/purview-audit.md`.

## Open gaps

| ID | Gap | Status | Impact |
|---|---|---|---|
| GAP-03 | Audit search returned `BadRequest` on the lab tenant (11 to 12 October 2026) | Resolved for the campaign: cmdlet search works after adding the admin account to Organization Management (12 October). Cause not fully isolated. | Closed on 24 October 2026: Exchange DLP events and Activity explorer events observed for TC-001, TC-002, TC-003a, TC-003b, TC-003c. Evidence limited to the trial period. |
| GAP-04 | Outbound mail to external recipients rejected with `550 5.7.501` on the trial tenant | Rejections observed on 15 October 2026 (12:19 to 12:28 UTC). Resolved later that day without a confirmed cause. | Closed on 15 October 2026: external delivery observed (SMOKE-001) and confirmed by message trace for TC-002, TC-003a, TC-003c and TC-001. |

### GAP-05: default sensitivity label applied to test messages and attachments

- Status: open, accepted for v0.3.
- Observed: `General\All Employees (unrestricted)` is applied automatically to every
  test message (Exchange) and attachment (endpoint), without user action.
- Impact: the label does not change the file bytes (SHA-256 verified on the received
  copies for TC-002 and TC-003a). Label-based scenarios are not validated.
- Decision: default labels kept for the v0.3 campaign (option A). Mapping of taxonomy
  L3 and L4 to Highly Confidential labels is documented as a gap, not implemented.
