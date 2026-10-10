# KPI and KRI

Indicators measure the effectiveness of the DLP control and the quality of policies. **They never rank or score individual employees.** Any per-user view is restricted to investigations under the triage playbook.

## Performance indicators (KPI)

| ID | Name | Definition | Formula | Source | Frequency | Owner | Target / threshold | Interpretation limit |
|---|---|---|---|---|---|---|---|---|
| KPI-01 | Alert volume | Alerts per policy and channel | count(alerts) by policy, channel | DLP alerts | Weekly | DLP Engineer | Trend, no fixed target | Volume depends on business activity; rises after scope extension |
| KPI-02 | False positive rate | Share of triaged alerts qualified FP | FP / triaged alerts | Triage records | Monthly | DLP Governance | below 10% per policy in production | Depends on triage consistency; sample-based for high volumes |
| KPI-03 | Justification rate | Share of blocks overridden with justification | overrides / (blocks with override option) | DLP events | Monthly | DLP Governance | Trend; investigate above 30% | High rate can mean a legitimate process not yet excepted |
| KPI-04 | Blocks | Blocked actions by policy and channel | count(block events) | DLP events | Monthly | DLP Engineer | Trend | Blocks are not incidents avoided with certainty |
| KPI-05 | Active exceptions | Number of active exceptions | count(status = Active) | Exception register | Monthly | DLP Governance | Trend | Low number can mean exceptions handled outside the process |
| KPI-06 | Mean time to triage | Alert creation to qualification | mean(triaged_at - created_at) | Case tool | Monthly | SOC | High: 1 business day | Weekend and holiday effects |
| KPI-07 | Mean time to close | Alert creation to closure | mean(closed_at - created_at) | Case tool | Monthly | SOC | High: 10 business days | Escalated cases take longer by design |
| KPI-08 | Endpoint coverage | Onboarded and healthy devices vs in-scope devices | healthy onboarded / in-scope | Endpoint DLP device health, asset inventory | Weekly | Endpoint team | above 98% | Inventory accuracy |
| KPI-09 | Policies by stage | Number of policies in S0 to S5 | count by stage | Policy specs | Monthly | DLP Governance | Plan-based | Stage is a maturity signal, not effectiveness |
| KPI-10 | Tuning effect | FP rate change after a tuning change | FP rate after - FP rate before (same regression set) | Test matrix, triage | Per change | DLP Engineer | Negative delta without new false negatives | Regression set must be stable to compare |

## Risk indicators (KRI)

| ID | Name | Definition | Formula | Source | Frequency | Owner | Threshold | Interpretation limit |
|---|---|---|---|---|---|---|---|---|
| KRI-01 | Confirmed high-severity events | TP-VIOL, TP-SUSP, TP-BREACH on L3/L4 data | count | Triage records | Monthly | CISO | Any TP-BREACH escalated to management | Detection coverage limits what can be seen |
| KRI-02 | Overdue exceptions | Exceptions past expiry still active | count(expiry < today and status = Active) | Exception register | Monthly | DLP Governance | 0 | Register must be reconciled with configuration |
| KRI-03 | Override rate on L4 rules | Overrides where only strict block should exist | count | DLP events | Monthly | CISO | 0 (indicates misconfiguration) | |
| KRI-04 | Uncovered channels | In-scope channels with no active policy | count | Coverage matrix | Quarterly | DLP Governance | Decreasing | Channel list must be complete |
| KRI-05 | Triage backlog | Untriaged High/Critical alerts older than target | count | Case tool | Weekly | SOC | 0 | |
