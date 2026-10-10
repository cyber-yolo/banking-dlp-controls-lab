## Summary

Closes #

## Type

- [ ] Use case / taxonomy
- [ ] Policy (Purview / Symantec)
- [ ] Test / generator
- [ ] Governance / regulatory
- [ ] CI / automation / docs

## Traceability

- Use case(s):
- Policy ID(s):
- Test case(s):
- Evidence reference (if a result is claimed):

## Security checklist (mandatory)

- [ ] No real personal, customer, employee or banking data
- [ ] No secret, token, password, certificate or connection string (except documented synthetic placeholders)
- [ ] No tenant ID, tenant domain, internal URL, client or employer name
- [ ] No screenshot from any environment other than the redacted personal lab
- [ ] No content describing how to bypass or disable a security control
- [ ] Generated files are not committed (`output/`, `evidence/` ignored)
- [ ] Regulatory statements cite the text and are marked TO VERIFY if not checked against the official source
- [ ] Untested items are labelled as such
- [ ] `python -m dlpgen validate-repo --root ..` passes locally
