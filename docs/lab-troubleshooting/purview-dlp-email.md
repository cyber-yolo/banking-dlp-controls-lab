# Troubleshooting: Purview DLP on Exchange email in a trial tenant

Observed during the v0.3 campaign (October 2026). Scope: external email from a new Microsoft 365 E5 trial tenant, one Exchange DLP policy (PV-POL-001) in simulation mode. Findings are limited to that setup and are not generalised.

## 1. External mail rejected with 550 5.7.501

### Symptom

- Outbound mail to an external mailbox is rejected with `550 5.7.501`.
- Internal mail works. Message trace shows the message as failed or quarantined at the outbound stage.
- Observed on 15 October 2026 between 12:19 and 12:28 UTC (SMOKE-001 attempts).

### Cause

Not confirmed. This status is typically an outbound anti-spam restriction applied to new trial tenants sending to external recipients. Microsoft did not confirm the reason for this tenant.

### What changed before it worked

- A custom domain was added to the tenant and used as the sender address (see section 2).
- External delivery then succeeded later the same day (SMOKE-001), and stayed reliable for TC-001, TC-002, TC-003a, TC-003b and TC-003c.
- The custom domain and any waiting period were not tested separately. Do not read this as proof that the domain is the fix.

### Recommendation

1. Check the message trace for the exact error before changing anything.
2. Use a custom domain as sender if the default `onmicrosoft.com` domain is rejected.
3. If it still fails, open a support request and keep the trace details. Do not retry in a loop.

## 2. Sending from a custom domain

General procedure, with no domain name published in this repository.

1. In the Microsoft 365 admin center, add the domain and complete the verification with the TXT record it provides.
2. Add the mail records the wizard asks for (MX, SPF) at the DNS provider. If the DNS provider proxies records, keep mail records on DNS only.
3. Assign the new domain to the test user as primary address.
4. Wait for propagation, then send a message to an external mailbox and check the message trace.

Lab domain hygiene:

- Keep WHOIS privacy enabled on the registrar.
- Never publish the lab domain, tenant name or user addresses in this repository. Use `user1@<lab-domain>` and `external-recipient@redacted.example` in evidence files.

## 3. Reading the results

### Activity Explorer

- The predefined filter set "DLP policy rules that detected activities" hid the events. Set the filter set to "None" to see them, and read the rule matched in the event detail.
- The detail does not expose the number of IBANs detected. For the R1 band (1 to 4 IBANs) only the band can be recorded, not the exact count. The CSV export has no count column either.
- Default sensitivity label events appear on every test message (see GAP-05 in `docs/02-assumptions-and-limits.md`).

### Alert mails

- Only rules with `GenerateAlert` set send a mail. In this setup R2 and R3 do, R1 does not.
- Absence of a mail for a one to four IBAN test is expected and is not a failure.

### Message trace

- The portal labels times as UTC+01:00, but the values displayed matched Paris local time. During summer time (until 25 October 2026) that is UTC+02:00. Convert before comparing with alert or Activity Explorer timestamps.
- Delivery status in the trace confirms delivery to the external mailbox, independent of DLP.

### Policy status

- In the configuration export, `DistributionStatus` stayed `Pending` while `DistributionSyncStatus` was `Success`, and the policy was effective in practice. See `docs/02-assumptions-and-limits.md`.
- Simulation mode (`TestWithoutNotifications`) does not enforce `BlockAccess`. A rule configured as block still delivers the message. The block action is not validated by this campaign.

## 4. After the trial ends

- When the subscription is disabled, mailbox access returns `TenantAccessBlockedException` and the compliance cmdlets disappear from the admin role definition. Evidence not exported before that point is lost.
- Export the configuration (`Export-DlpConfiguration.ps1`) and the Activity Explorer data before the end of the trial.
