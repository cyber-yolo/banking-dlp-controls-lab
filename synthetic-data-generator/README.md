# Synthetic data generator (`dlpgen`)

Produces fictitious banking files for DLP testing, from a seeded, scenario-based configuration. The corpus is **never committed**: it is rebuilt on demand and identified by its manifest and SHA-256 hashes.

## Commands

```bash
python -m dlpgen generate --config config.example.yaml          # build corpus + manifest.json/.csv
python -m dlpgen validate-output --manifest output/manifest.json # hashes + markers in every file
python -m dlpgen validate-repo --root ..                         # scan versioned files for real-looking data
python -m dlpgen clean --output output                           # delete corpus (only if created by dlpgen)
python -m pytest -q                                              # unit tests
```

## Design

| Concern | Decision |
|---|---|
| Reproducibility | One RNG per scenario seeded with `seed:scenario_id`. Office formats are normalised (fixed ZIP entry dates and document properties) and PDFs use invariant mode, so **the same config gives the same SHA-256 for every file, in every format**. |
| Traceability | `manifest.json` and `manifest.csv` record file ID, scenario, use case, test type, seed, categories, exact occurrence counts, expected policy, action, alert and result, hash. |
| Markers | Every file carries `SYNTHETIC TEST DATA`, `NOT A REAL CUSTOMER`, `FOR DLP TESTING ONLY` in content, and in metadata where the format allows. |
| Marker vs detection | The marker text contains the word CUSTOMER. Detector keyword lists therefore must not use "customer", otherwise the marker itself would provide context and break context tests. A unit test enforces this against the custom SIT rule package. |
| Format-specific expectations | `format_overrides` lets a scenario state that, for example, the PNG version is not expected to match without OCR. |
| Safety | `generate` refuses to overwrite a non-empty folder it did not create; `clean` refuses to delete one. |

## Value rules

| Data | Rule | Why |
|---|---|---|
| IBAN CH/LU | Checksum-valid, zero bank code, `SYNTH` in the account part | Detectors validate mod 97; no official test range exists; `SYNTH` makes collision with a real account practically impossible |
| Invalid IBAN | Same structure, wrong check digits | False-positive tests only |
| Card numbers | Publicly documented processor test numbers only | Luhn-valid, never issued |
| BIC | `SYN?` + country + `Z0` + `XXX` | A `0` in second position of the location code is the SWIFT test BIC convention |
| Client ID / portfolio ID | `CLT-########`, `PF-##-######` | Match the lab custom SITs |
| Names, addresses | Fixed fictitious lists, invalid postal codes | Names can coincide with real people; documents are marked |
| Secrets | Publicly documented non-functional examples | Must never be real |
| AHV/AVS, LU national ID | Not generated | Any checksum-valid value could be a real person |

## Scenario types

`positive`, `negative`, `boundary-below`, `boundary-at`, `boundary-above`, `context-without`, `context-with`, `multi-data`, `false-positive`. Exception and channel tests reuse the same files with a different recipient, device or channel, recorded in `testing/test-matrix.csv`.

## Categories

`iban`, `iban_invalid`, `client_id`, `card_pan`, `kyc`, `aml`, `secrets`, `portfolio`, `transactions`, `hr_salary`, `negative`.
