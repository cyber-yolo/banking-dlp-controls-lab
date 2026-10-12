# Troubleshooting: Purview Audit search on a new trial tenant

## Symptom

- Purview and Defender Audit > Search show "Sorry, we're having trouble figuring out if activity is being recorded"
- Audit search list shows "Failed to load data"
- `Search-UnifiedAuditLog` returns `WARNING: Failed to process request via Sync Search mode ... BadRequest`
- `Get-AdminAuditLogConfig` shows `UnifiedAuditLogIngestionEnabled : True`

## Root cause (probable, not isolated)

The "Audit Logs" role was reachable only through the built-in *Organization Management* role group, and the admin account was not a member. A custom Purview role group containing "Audit Logs" does not grant the Exchange cmdlets. Adding the account to *Organization Management* made `Search-UnifiedAuditLog` return results on the same day, with no other change. Propagation time may also have contributed; the fix was not isolated.

## Fix

Check membership:

```powershell
Get-RoleGroupMember "Organization Management"
```

If the admin account is missing, add it:

```powershell
Add-RoleGroupMember "Organization Management" -Member "<admin-upn>"
```

Then disconnect, reconnect, and wait up to one hour before concluding.

Verify:

```powershell
Search-UnifiedAuditLog -StartDate "<today-1>" -EndDate "<today>" -ResultSize 5
```

## Pitfalls

- Global Administrator alone did not give cmdlet access to the audit search in this tenant.
- `Connect-ExchangeOnline` on Windows PowerShell 5.1 may fail with PackageManagement conflicts. Use PowerShell 7 (`winget install Microsoft.PowerShell`).
- A search job in the portal can stay "Queued" for a while. Do not start a second unfiltered search in parallel.
- Search results on a new tenant can initially show only Entra ID records. Exchange and SharePoint events need activity and a 60 to 90 minute ingestion delay.

## Related

- Activity Explorer uses a separate read path from Audit Search and is needed for DLP evidence.
- See GAP-03 in `docs/02-assumptions-and-limits.md`.
