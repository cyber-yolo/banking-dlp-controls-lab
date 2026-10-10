import random
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from dlpgen import values as v

RULEPACK = Path(__file__).resolve().parents[2] / "platforms" / "microsoft-purview" / "custom-sits" / "banking-lab-sit-rulepack.xml"
NS = {"m": "http://schemas.microsoft.com/office/2011/mce"}


@pytest.mark.parametrize("country,length", [("CH", 21), ("LU", 20)])
def test_synthetic_iban_is_valid_and_marked(country, length):
    rng = random.Random(1)
    for _ in range(200):
        iban = v.synthetic_iban(rng, country)
        assert len(iban) == length
        assert iban.startswith(country)
        assert v.iban_is_valid(iban)
        assert v.SYNTH_TAG in iban


@pytest.mark.parametrize("country", ["CH", "LU"])
def test_invalid_iban_fails_checksum(country):
    rng = random.Random(2)
    for _ in range(200):
        assert not v.iban_is_valid(v.invalid_iban(rng, country))


def test_iban_generation_is_deterministic():
    a = [v.synthetic_iban(random.Random("s:1"), "CH") for _ in range(3)]
    b = [v.synthetic_iban(random.Random("s:1"), "CH") for _ in range(3)]
    assert a == b


def test_grouped_format_keeps_validity():
    iban = v.synthetic_iban(random.Random(3), "LU")
    assert v.iban_is_valid(v.format_iban(iban, grouped=True))


def test_test_pans_are_luhn_valid():
    assert all(v.luhn_is_valid(p) for p in v.ALL_TEST_PANS)


def test_bic_uses_test_location_convention():
    bic = v.sample_test_bic(random.Random(4), "CH")
    assert len(bic) == 11 and bic[4:6] == "CH" and bic[7] == "0"


def test_rulepack_regexes_match_generated_ids():
    root = ET.parse(RULEPACK).getroot()
    regexes = {r.get("id"): r.text for r in root.iter("{%s}Regex" % NS["m"])}
    rng = random.Random(5)
    assert re.fullmatch(regexes["Regex_client_id"].replace("\\b", ""), v.client_id(rng))
    assert re.fullmatch(regexes["Regex_portfolio_id"].replace("\\b", ""), v.portfolio_id(rng))


def test_banner_contains_no_detector_keyword():
    """The mandatory marker must not give context to keyword-based detectors."""
    root = ET.parse(RULEPACK).getroot()
    terms = [t.text.lower() for t in root.iter("{%s}Term" % NS["m"])]
    banner_words = set(re.findall(r"[a-z]+", v.BANNER.lower()))
    offending = [t for t in terms if set(t.split()) <= banner_words]
    assert not offending, f"banner provides detector context: {offending}"
