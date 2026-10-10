# Regulatory mapping methodology

## Rule

A DLP configuration is **never** presented as a legal obligation unless the text requires that specific measure. Texts require outcomes (confidentiality, security of processing, protection of information assets, secrecy); DLP is one possible technical control among others. Each mapping row separates:

| Column | Content |
|---|---|
| Regulatory requirement | What the text requires, in own words, with exact reference |
| Banking risk | The risk the requirement addresses in a bank |
| Control objective | CO-xx (vendor-agnostic) |
| Organisational control | Policy, process, role, training |
| Technical DLP control | UC-xxx and its detection and action intent |
| Vendor configuration | PV-POL-xxx / SY-POL-xxx |
| Control limit | What DLP does not cover for this requirement |
| Audit evidence | What an auditor can inspect |
| Validation owner | Legal, Compliance, Privacy, Risk, Information Security |
| Verification status | TO VERIFY until checked against the official consolidated text |

## Applicability notes

| Topic | Note |
|---|---|
| DORA vs NIS2 | For EU financial entities in scope of DORA, DORA applies as the sector-specific act for ICT risk management; NIS2 is kept as context. Confirm national transposition specifics. |
| DORA and Swiss banks | DORA does not apply directly to Swiss banks; it may apply to their EU subsidiaries or through contracts with EU clients. |
| EBA and CSSF | EBA guidelines on ICT and security risk management were transposed in Luxembourg by CSSF circular; their interplay with DORA for entities in DORA scope must be checked in the current CSSF texts. |
| FINMA | FINMA circular on operational risks and resilience for banks includes expectations on critical data; exact marginal numbers to be cited after verification. |
| Employee monitoring | DLP processes employee data. Luxembourg labour law and the Swiss nLPD and labour law impose conditions (information, consultation, proportionality). These are prerequisites to deploy DLP, mapped as constraints, not as DLP controls. |

## Verification procedure

1. Retrieve the official consolidated text (EUR-Lex, Legilux, Fedlex, CSSF, FINMA, EBA websites).
2. Confirm article or marginal number, and quote nothing longer than needed.
3. Record source URL and consultation date in the row.
4. Change status to VERIFIED and have Legal or Compliance review wording if used externally.
