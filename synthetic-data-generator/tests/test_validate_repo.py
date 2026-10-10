from dlpgen import values as v
from dlpgen.validate import scan_text


def _real_looking_iban():
    bban = "12345" + "678901234567"
    return "CH" + v.iban_check_digits("CH", bban) + bban


def _luhn_complete(prefix):
    for d in "0123456789":
        if v.luhn_is_valid(prefix + d):
            return prefix + d
    raise AssertionError


def test_flags_checksum_valid_iban_without_marker():
    findings = scan_text(f"account {_real_looking_iban()} here")
    assert [f.rule for f in findings] == ["iban"]


def test_accepts_synthetic_iban():
    import random

    assert scan_text(v.synthetic_iban(random.Random(0), "LU")) == []


def test_flags_non_test_pan_and_accepts_test_pan():
    assert [f.rule for f in scan_text(_luhn_complete("400000000000123"))] == ["pan"]
    assert scan_text("4111 1111 1111 1111") == []


def test_email_domains():
    assert scan_text("a.b@client.synthbank.example") == []
    assert [f.rule for f in scan_text("a.b@" + "realbank" + ".com")] == ["email"]


def test_tenant_domain_and_keys():
    assert [f.rule for f in scan_text("admin@" + "acmebank" + ".onmicrosoft.com")] == ["email", "tenant"]
    assert scan_text(v.AWS_EXAMPLE_ACCESS_KEY) == []
    assert [f.rule for f in scan_text("AKIA" + "Q" * 16)] == ["aws-key"]
    assert [f.rule for f in scan_text("-----BEGIN " + "RSA PRIVATE KEY-----")] == ["private-key"]
