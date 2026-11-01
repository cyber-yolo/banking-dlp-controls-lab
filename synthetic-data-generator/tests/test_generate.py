import json
import re
from pathlib import Path

import pytest

from dlpgen import values as v
from dlpgen.generate import clean, generate
from dlpgen.validate import validate_output

CONFIG = Path(__file__).resolve().parents[1] / "config.example.yaml"
RE_IBAN = re.compile(r"\b(?:CH|LU)\d{2}[0-9A-Z]{16,17}\b")


@pytest.fixture(scope="module")
def corpus(tmp_path_factory):
    out = tmp_path_factory.mktemp("corpus")
    manifest = generate(CONFIG, out)
    return out, json.loads(manifest.read_text())


def _valid_ibans(text):
    return [m for m in RE_IBAN.findall(text) if v.iban_is_valid(m)]


def test_output_validates(corpus):
    out, _ = corpus
    assert validate_output(out / "manifest.json") == []


def test_same_seed_same_hashes_all_formats(corpus, tmp_path):
    _, first = corpus
    second = json.loads(generate(CONFIG, tmp_path / "again").read_text())
    h1 = {f["file_name"]: f["sha256"] for f in first["files"]}
    h2 = {f["file_name"]: f["sha256"] for f in second["files"]}
    assert h1 == h2


@pytest.mark.parametrize("scenario,expected", [("SCN-002", 4), ("SCN-003", 5), ("SCN-011", 20), ("SCN-001", 10)])
def test_boundary_counts_are_exact(corpus, scenario, expected):
    out, _ = corpus
    text = next(out.glob(f"{scenario}_*.txt")).read_text()
    assert len(_valid_ibans(text)) == expected


def test_negative_and_false_positive_have_no_valid_iban(corpus):
    out, _ = corpus
    for scenario in ("SCN-004", "SCN-005"):
        text = next(out.glob(f"{scenario}_*.txt")).read_text()
        assert _valid_ibans(text) == []
        assert "CLT-" not in text


def test_context_without_has_no_keywords(corpus):
    out, _ = corpus
    text = next(out.glob("SCN-006_*.txt")).read_text().lower()
    assert "client" not in text and "relationship manager" not in text


def test_manifest_occurrences_match(corpus):
    _, manifest = corpus
    entry = next(f for f in manifest["files"] if f["file_id"] == "SCN-009-TXT")
    assert entry["occurrences"] == {"kyc_record": 3, "client_id": 3, "iban": 2}


def test_format_override_applied(corpus):
    _, manifest = corpus
    png = next(f for f in manifest["files"] if f["file_id"] == "SCN-001-PNG")
    assert png["expected_action"] == "none"


def test_clean_refuses_foreign_folder(tmp_path):
    (tmp_path / "keep.txt").write_text("not generated")
    with pytest.raises(RuntimeError):
        clean(tmp_path)


def test_aml_training_has_vocabulary_but_no_client_id(corpus):
    out, manifest = corpus
    text = next(out.glob("SCN-014_*.txt")).read_text()
    assert "CLT-" not in text
    assert all(term in text for term in ("suspicious transaction report", "CRF", "money laundering"))
    entry = next(f for f in manifest["files"] if f["file_id"] == "SCN-014-TXT")
    assert entry["occurrences"] == {"aml_training_module": 5}
