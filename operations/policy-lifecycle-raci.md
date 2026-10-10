# Policy lifecycle and RACI

## Lifecycle

| # | Stage | Output | Gate |
|---|---|---|---|
| 1 | Request | Issue (use case or policy form) | Business owner identified |
| 2 | Needs analysis | Risk, data, channel, population, volume estimate | DLP Governance accepts |
| 3 | Business validation | Thresholds and exceptions agreed | Business owner sign-off |
| 4 | Privacy and legal review | Proportionality, employee information, DPIA need, works council / staff delegation consultation where required | DPO and Legal sign-off |
| 5 | Design | Policy spec (`PV-POL-xxx.yaml`) | Peer review |
| 6 | Test | Test matrix rows PASS | Evidence complete |
| 7 | Simulation (S1, S2) | Match statistics, FP rate | Exit criteria met |
| 8 | Pilot (S3) | Pilot report | No business-blocking incident |
| 9 | Production (S4, S5) | Change record | Owner and CISO approval |
| 10 | Tuning | Change PR with before/after metrics | Regression PASS |
| 11 | Periodic review | Review record | Owner confirms still needed |
| 12 | Retirement | Policy disabled then removed, evidence archived | Owner approval |

## RACI

R = Responsible, A = Accountable, C = Consulted, I = Informed.

| Activity | DLP Engineer | DLP Governance | Business Owner | DPO / Privacy | Legal | Compliance | CISO | SOC | HR | Staff representatives |
|---|---|---|---|---|---|---|---|---|---|---|
| New rule request | I | R | A | I | | C | I | | | |
| Needs analysis | C | R | A | C | | C | I | | | |
| Privacy and legal review | I | R | C | A | R | C | I | | C | C |
| Policy design | R | A | C | C | | C | I | C | | |
| Testing | R | A | C | | | | I | | | |
| Simulation and pilot | R | A | C | I | | I | I | C | I | I |
| Production go-live | R | C | C | I | I | I | A | I | I | I |
| Alert triage | C | I | | | | | I | R/A | | |
| Investigation of an employee | | C | C | C | C | C | A | R | R | |
| Exception approval | I | R | A | C | | C | C | | | |
| Tuning | R | A | C | | | | I | C | | |
| Periodic review | C | R | A | C | | C | I | | | |
| Retirement | R | R | A | I | | I | I | I | | |

Luxembourg note: monitoring employees' electronic communications is subject to specific labour-law conditions (information and consultation of staff representatives). Swiss note: employee monitoring must respect proportionality under the nLPD and labour law. Both are prerequisites to go-live, not DLP settings. References are listed in `regulatory-mapping/mapping.csv` (to verify).
