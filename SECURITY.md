# Security policy

## Scope

This repository contains documentation, synthetic test data tooling and lab scripts. It must never contain real personal data, banking data, secrets or client configurations.

## Reporting

If you find real data, a secret, a tenant identifier or any content that could identify a real organisation or person:

1. Do **not** open a public issue quoting it.
2. Use GitHub private vulnerability reporting (Security tab > Report a vulnerability).
3. The maintainer will remove the content, rewrite history if needed (`git filter-repo`), rotate anything exposed and document the incident without reproducing the data.

Target response: acknowledgement within 5 working days.

## Preventive controls

| Control | Where |
|---|---|
| Secret scanning and push protection | GitHub repository settings |
| gitleaks on every push and PR | `.github/workflows/ci.yml`, `.gitleaks.toml` |
| Repo data validator (checksum-valid IBANs without synthetic marker, non-test PANs, private keys, non-example email domains, tenant domains) | `python -m dlpgen validate-repo` |
| Generated corpus and lab evidence git-ignored | `.gitignore` |
| PR security checklist | `.github/pull_request_template.md` |

## Out of scope

Techniques to evade DLP detection are out of scope and will not be accepted, including under a "red team" label.
