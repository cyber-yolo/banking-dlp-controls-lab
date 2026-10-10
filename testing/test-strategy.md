# Test strategy

## Categories

| Category | Question answered | Generator scenario |
|---|---|---|
| Positive | Does the policy fire on what it must catch? | SCN-001, 008, 010, 012, 013 |
| Negative | Does it stay silent on clean content? | SCN-004 |
| Boundary | Is the threshold exactly where the spec says? | SCN-002 (below), SCN-003 (at), SCN-011 (above) |
| Context | Does keyword context change confidence as designed? | SCN-006 (without), SCN-007 (with) |
| Multi-data | Do combined categories raise the right rule? | SCN-009 |
| Exception | Does an approved exception allow the flow and log it? | SCN-001 to an approved domain |
| False positive | Is look-alike data ignored? | SCN-005 (wrong checksums) |
| False negative | Where can an expected detection be missed? | SCN-001 PNG (no OCR), password-protected archives, unsupported browser |
| Channel | Same file, different channel: same decision? | SCN-001 via email, SharePoint, USB, browser upload |
| Regression | Did a policy change alter any previous result? | Full manifest replay |

## Execution protocol

1. Generate the corpus: `python -m dlpgen generate --config config.example.yaml`. Record the manifest `config_sha256`.
2. Check the policy stage and mode in the lab; export configuration with `Export-DlpConfiguration.ps1` (evidence of configuration at test time).
3. Execute the action on the target channel with the file listed in the test case. Record UTC timestamp.
4. Allow for policy distribution and event ingestion before concluding. Record the wait time.
5. Collect: user-side result (tip, block, notification), Activity Explorer event, alert (if expected).
6. Store evidence in `evidence/<TC-ID>/<timestamp>/` with SHA-256; commit only redacted extracts.
7. Fill the test matrix row: actual result, status, evidence reference.

## Pass criteria

A test passes when action, alert and severity all match the expected values in the manifest. A partial match (for example correct block, wrong severity) is `FAIL` with a comment, never `PASS`.

## Status values

`NOT RUN`, `PASS`, `FAIL`, `BLOCKED` (prerequisite missing, for example no licence), `N/A` (not applicable to this platform).

## Regression

After any policy change: replay every test linked to the policy, plus all negative and false-positive tests. Compare with the previous run by file hash and expected result. Any difference is either an intended change (documented in the PR) or a regression.
