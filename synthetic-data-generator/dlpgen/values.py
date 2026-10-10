"""Synthetic value factories.

Design rules
------------
* IBANs are checksum-valid (ISO 7064 mod 97-10) so that checksum-validating detectors
  fire, but use a zero bank code and the literal ``SYNTH`` in the account part, which
  makes a collision with a real account practically impossible. There is no official
  IBAN test range; the residual risk is documented, not eliminated.
* Card numbers come only from publicly documented payment-processor test numbers.
* BICs use a location code whose second character is ``0``, the SWIFT convention for
  test and training BICs, and the fictitious institution code ``SYN?``.
* Secrets are publicly documented, non-functional examples.
* National ID numbers (AHV/AVS, Luxembourg matricule) are deliberately NOT generated:
  any checksum-valid value could belong to a real person.
"""

from __future__ import annotations

import random
import string
from datetime import date, timedelta

MARKERS = ("SYNTHETIC TEST DATA", "NOT A REAL CUSTOMER", "FOR DLP TESTING ONLY")
BANNER = " | ".join(MARKERS)
SYNTH_TAG = "SYNTH"

IBAN_LAYOUT = {
    # country: (bank code length, account length, total length)
    "CH": (5, 12, 21),
    "LU": (3, 13, 20),
}

TEST_PANS = {
    "visa": ("4111111111111111", "4012888888881881"),
    "mastercard": ("5555555555554444", "5105105105105100"),
    "amex": ("378282246310005", "371449635398431"),
}
ALL_TEST_PANS = frozenset(p for pans in TEST_PANS.values() for p in pans)

AWS_EXAMPLE_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_EXAMPLE_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

FIRST_NAMES = (
    "Aline", "Bastien", "Clea", "Dorian", "Elsa", "Fabian", "Gaelle", "Hugo", "Ines", "Joris",
    "Katia", "Lionel", "Maelle", "Nils", "Oriane", "Pascal", "Quentin", "Romane", "Silvan", "Tessa",
)
LAST_NAMES = (
    "Albrecht", "Bernasconi", "Clement", "Dufresne", "Eberhard", "Fontaine", "Gerber", "Hoffmann",
    "Jacquet", "Keller", "Lambert", "Marchetti", "Nussbaum", "Oberlin", "Perret", "Reuter",
    "Schaller", "Thill", "Vogt", "Weber",
)
# Postal codes are outside the real ranges on purpose.
ADDRESSES = {
    "CH": (("Musterstrasse", "0000", "Beispielstadt"), ("Rue Fictive", "0001", "Exempleville")),
    "LU": (("Rue de l'Exemple", "L-0000", "Synthville"), ("Route Imaginaire", "L-0001", "Testange")),
}
CURRENCY = {"CH": "CHF", "LU": "EUR"}


def _to_digits(text: str) -> str:
    return "".join(str(int(ch, 36)) for ch in text)


def iban_check_digits(country: str, bban: str) -> str:
    remainder = int(_to_digits(bban + country + "00")) % 97
    return f"{98 - remainder:02d}"


def iban_is_valid(iban: str) -> bool:
    compact = iban.replace(" ", "").upper()
    if len(compact) < 5 or not compact[:2].isalpha() or not compact[2:4].isdigit():
        return False
    if not compact.isalnum():
        return False
    return int(_to_digits(compact[4:] + compact[:4])) % 97 == 1


def synthetic_iban(rng: random.Random, country: str) -> str:
    bank_len, acct_len, total = IBAN_LAYOUT[country]
    digits = acct_len - len(SYNTH_TAG)
    account = SYNTH_TAG + "".join(rng.choice(string.digits) for _ in range(digits))
    bban = "0" * bank_len + account
    iban = country + iban_check_digits(country, bban) + bban
    assert len(iban) == total and iban_is_valid(iban)
    return iban


def invalid_iban(rng: random.Random, country: str) -> str:
    """Same structure as synthetic_iban but with a wrong checksum (false-positive tests)."""
    valid = synthetic_iban(rng, country)
    check = int(valid[2:4])
    wrong = check + 1 if check < 98 else check - 1
    result = f"{valid[:2]}{wrong:02d}{valid[4:]}"
    assert not iban_is_valid(result)
    return result


def format_iban(iban: str, grouped: bool = False) -> str:
    if not grouped:
        return iban
    return " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))


def luhn_is_valid(number: str) -> bool:
    digits = [int(d) for d in number if d.isdigit()]
    if len(digits) < 12:
        return False
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def sample_test_pan(rng: random.Random) -> str:
    return rng.choice(sorted(ALL_TEST_PANS))


def sample_test_bic(rng: random.Random, country: str) -> str:
    return f"SYN{rng.choice(string.ascii_uppercase)}{country}Z0XXX"


def client_id(rng: random.Random) -> str:
    return f"CLT-{rng.randint(0, 99_999_999):08d}"


def portfolio_id(rng: random.Random) -> str:
    return f"PF-{rng.randint(10, 99)}-{rng.randint(0, 999_999):06d}"


def person(rng: random.Random, country: str) -> dict:
    first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
    street, postcode, city = rng.choice(ADDRESSES[country])
    dob = date(1950, 1, 1) + timedelta(days=rng.randint(0, 18_000))
    return {
        "name": f"{first} {last}",
        "address": f"{street} {rng.randint(1, 99)}, {postcode} {city}",
        "date_of_birth": dob.isoformat(),
        "email": f"{first}.{last}@client.synthbank.example".lower(),
    }


def amount(rng: random.Random, low: int = 100, high: int = 250_000) -> str:
    return f"{rng.randint(low, high)}.{rng.randint(0, 99):02d}"


def fake_secrets() -> list[str]:
    return [
        f"aws_access_key_id = {AWS_EXAMPLE_ACCESS_KEY}",
        f"aws_secret_access_key = {AWS_EXAMPLE_SECRET_KEY}",
        "Server=db01.synthbank.example;Database=core_synth;User Id=svc_synth;Password=NOT-A-REAL-SECRET;",
        "api_token: NOT-A-REAL-SECRET-0000000000000000",
    ]
