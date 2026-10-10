# Exception management

An exception is a documented, approved and time-bound deviation from a DLP policy. It is not a permanent policy change: if an exception is renewed twice, the policy itself should be reviewed.

## Required fields

| Field | Rule |
|---|---|
| ID | `EXC-YYYY-###` |
| Policy / rule | Specific rule, never "all DLP" |
| Scope | Named users or group, named destination (domain, device group, app), data category |
| Business justification | Written by the business owner |
| Risk assessment | Residual risk after compensating controls |
| Compensating control | For example encryption, approved channel, monthly sample review |
| Approver | Business owner + DLP Governance; CISO for L4 data |
| Start / expiry | Maximum 6 months (L3), 3 months (L4) |
| Review | Before expiry; expired exceptions are removed automatically or by the next review cycle |

## Implementation

Exceptions are implemented as narrow policy exclusions (recipient domain, device group, user group). Each exclusion references its EXC ID in the rule comment so a configuration export can be reconciled with the register (`exceptions-register.csv`).

## Indicators

Active exceptions, exceptions by age, exceptions past expiry (KRI-02). See `dashboards/kpi-kri.md`.
