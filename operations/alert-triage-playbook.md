# Alert triage and investigation playbook

## Principles

- Minimise access to content: analysts see match metadata first; content viewing is a separate, logged role.
- Never contact the client about an AML-related alert (tipping-off).
- An employee investigation starts only with HR and Legal involvement, not from the DLP console alone.

## 1. Triage (target: within 1 business day for High and Critical)

| Step | Action |
|---|---|
| 1.1 | Check alert metadata: policy, rule, severity, user, channel, recipient or destination, count of matches |
| 1.2 | Check for an active exception (register) covering user, destination and data |
| 1.3 | Check if the user justified (override) and read the justification |
| 1.4 | Assign a qualification code (below) or escalate for content review |

## 2. Qualification codes

| Code | Meaning | Typical closure |
|---|---|---|
| FP | Detector matched non-sensitive content | Tuning ticket |
| TP-AUTH | Sensitive data, authorised business flow | Close; consider exception |
| TP-JUST | Sensitive data, justified override, justification acceptable | Close; sample review |
| TP-VIOL | Sensitive data, policy violation, no malicious indication | Manager and user awareness |
| TP-SUSP | Possible deliberate exfiltration | Escalate |
| TP-BREACH | Data actually left to an unauthorised party | Escalate for breach assessment |

## 3. Evidence collection

Collect only what is needed: alert ID, event export, policy version (configuration export hash), file hash if retained, user justification, timeline. Store in the case management tool with restricted access; record SHA-256 of exported evidence.

## 4. Escalation matrix

| Situation | Escalate to | Time target |
|---|---|---|
| TP-BREACH with personal data | DPO (GDPR / nLPD breach assessment) | Same day |
| Client data under Swiss banking secrecy or LU professional secrecy disclosed | Legal and Compliance | Same day |
| AML-related content (UC-010) | MLRO delegate only | Same day |
| TP-SUSP, leaver in scope (UC-009) | HR, Legal, CISO | 1 business day |
| Credentials exposed (UC-014) | SOC, system owner (rotation) | Immediately |
| Outsourcing or third-party flow (UC-011) | Vendor management, Compliance | 2 business days |
| Repeated FP on a rule | DLP Engineer (tuning) | Next tuning cycle |

GDPR requires notification to the supervisory authority within 72 hours of awareness when the breach is notifiable; the Swiss nLPD requires notification to the FDPIC as soon as possible when the breach is likely to result in a high risk. The DPO decides; the DLP team supplies facts.

## 5. Closure

Closure requires: qualification code, rationale, actions taken, links to exception or tuning ticket, and for TP-BREACH the reference of the breach assessment.
