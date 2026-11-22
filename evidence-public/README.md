# Public evidence

Redacted extracts from the Purview lab campaign (v0.3). Raw captures stay in the
git-ignored `evidence/` folder and are never committed.

## Redaction rules for screenshots

- Lab domain, tenant ID and the Gmail local part are covered with opaque boxes or erased.
- Alert IDs, policy IDs, record IDs and mailbox item IDs are covered with opaque boxes.
- User, sender and recipient fields are masked when they show the lab domain.
- PNG metadata is stripped.

## Screenshot index

| Run | Screenshot | Shows |
| --- | --- | --- |
| SMOKE-001 | [alert-20261015T1356Z.png](test-runs/SMOKE-001/alert-20261015T1356Z.png) | Alert mail, Medium, PV-POL-001-R2, IBAN count 5 |
| SMOKE-001 | [alert-20261015T1358Z.png](test-runs/SMOKE-001/alert-20261015T1358Z.png) | Alert mail, Medium, PV-POL-001-R2, IBAN count 5 |
| SMOKE-001 (context) | [alerts-list-20261013.png](test-runs/SMOKE-001/alerts-list-20261013.png) | Purview Alerts list, subject 'test', Low, 13 October (see run sheet) |
| TC-001 | [alert-20261024T2307Z.png](test-runs/TC-001/alert-20261024T2307Z.png) | Alert mail, Medium, PV-POL-001-R2, IBAN count 10 |
| TC-002 (SCN-004) | [sent-item-20261023T1913Z.png](test-runs/TC-002/sent-item-20261023T1913Z.png) | Sent item with SCN-004 negative attachment and General label |
| TC-003a, TC-002 | [activity-explorer-20261023-20261024.png](test-runs/TC-003a/activity-explorer-20261023-20261024.png) | Activity explorer: DLP rule matched (R1) on SCN-002, Label applied events |
| TC-003a, TC-002 | [message-trace-20261023-20261024.png](test-runs/TC-003a/message-trace-20261023-20261024.png) | Message trace: TC-003a and TC-002 Delivered |
| TC-003a | [activity-explorer-detail-20261023T2208Z.png](test-runs/TC-003a/activity-explorer-detail-20261023T2208Z.png) | Activity explorer detail: DLP rule matched, PV-POL-001-R1, subject TC-003a |
| TC-003a | [activity-explorer-location-20261023T2208Z.png](test-runs/TC-003a/activity-explorer-location-20261023T2208Z.png) | Activity explorer detail: IncludeExternalUsers, Exchange, attachment 38 KB |
| TC-003a | [activity-explorer-filtered-20261024-20261025.png](test-runs/TC-003a/activity-explorer-filtered-20261024-20261025.png) | Activity explorer, filter "DLP policies that detected activities", 3 items |
| TC-003c | [alert-20261024T2238Z.png](test-runs/TC-003c/alert-20261024T2238Z.png) | Alert mail, High, PV-POL-001-R3, IBAN count 20 |
| TC-003c | [message-trace-20261024T2237Z.png](test-runs/TC-003c/message-trace-20261024T2237Z.png) | Message trace: TC-003c Delivered |

TC-003b has no screenshot yet (Activity explorer capture pending).
