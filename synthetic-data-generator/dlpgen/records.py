"""Builds the in-memory document model for a scenario from data categories."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from dlpgen import values as v


@dataclass
class Section:
    heading: str
    headers: list[str]
    rows: list[list[str]]


@dataclass
class Document:
    title: str
    context: str | None
    sections: list[Section] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def lines(self) -> list[str]:
        out = [v.BANNER, "", self.title, ""]
        if self.context:
            out += [self.context, ""]
        for section in self.sections:
            out.append(section.heading)
            out.append(" | ".join(section.headers))
            out += [" | ".join(row) for row in section.rows]
            out.append("")
        out += self.notes
        out += ["", v.BANNER]
        return out


def _iban_section(rng, n, country, grouped, valid=True):
    rows = []
    for _ in range(n):
        p = v.person(rng, country)
        iban = v.synthetic_iban(rng, country) if valid else v.invalid_iban(rng, country)
        rows.append([p["name"], v.format_iban(iban, grouped), v.sample_test_bic(rng, country), v.CURRENCY[country]])
    return ["Account holder", "IBAN", "BIC", "Currency"], rows


def build_iban(rng, n, country, opts):
    headers, rows = _iban_section(rng, n, country, opts.get("iban_grouped", False))
    ctx = "Client account list prepared by the relationship manager for the quarterly client review."
    return "Client account extract", ctx, [Section("Client accounts", headers, rows)], [], {"iban": n}


def build_iban_invalid(rng, n, country, opts):
    headers, rows = _iban_section(rng, n, country, opts.get("iban_grouped", False), valid=False)
    ctx = "Reference list with account-like strings whose check digits are intentionally wrong."
    return "Reference list", ctx, [Section("References", headers, rows)], [], {"iban_invalid": n}


def build_client_id(rng, n, country, opts):
    rows = [[v.client_id(rng), v.person(rng, country)["name"], rng.choice(["Retail", "Private", "Corporate"])] for _ in range(n)]
    ctx = "Client ID list for the relationship manager review of the client book."
    return "Client list", ctx, [Section("Clients", ["Client ID", "Client name", "Segment"], rows)], [], {"client_id": n}


def build_card_pan(rng, n, country, opts):
    rows = [[v.person(rng, country)["name"], v.sample_test_pan(rng), "12/30"] for _ in range(n)]
    ctx = "Card replacement requests for client service follow-up."
    return "Card requests", ctx, [Section("Cards", ["Cardholder", "Card number", "Expiry"], rows)], [], {"card_pan": n}


def build_kyc(rng, n, country, opts):
    rows = []
    for _ in range(n):
        p = v.person(rng, country)
        rows.append([
            v.client_id(rng), p["name"], p["date_of_birth"], p["address"],
            f"SYN-DOC-{rng.randint(0, 999_999):06d}", rng.choice(["Low", "Medium", "High"]),
            rng.choice(["No", "No", "Yes"]), rng.choice(["Inheritance", "Business sale", "Salary", "Real estate"]),
        ])
    headers = ["Client ID", "Name", "Date of birth", "Address", "ID document", "Risk rating", "PEP", "Source of wealth"]
    ctx = "KYC periodic review dossier. Client due diligence summary submitted for compliance approval."
    return "KYC review dossier", ctx, [Section("Client due diligence", headers, rows)], [], {"kyc_record": n, "client_id": n}


def build_aml(rng, n, country, opts):
    fiu = "CRF" if country == "LU" else "MROS"
    rows, notes = [], []
    for i in range(n):
        cid = v.client_id(rng)
        rows.append([f"ALR-SYN-{rng.randint(0, 99_999):05d}", cid, rng.choice(["Structuring", "Rapid movement of funds", "High-risk jurisdiction"]), "Suspicious transaction report in preparation"])
        notes.append(f"Investigation memo {i + 1}: the compliance team is preparing a suspicious transaction report to the {fiu} regarding client {cid}. Do not inform the client.")
    ctx = "Internal AML investigation summary. Restricted to the compliance team."
    return "AML investigation summary", ctx, [Section("Alerts", ["Alert ID", "Client ID", "Scenario", "Status"], rows)], notes, {"aml_alert": n, "client_id": n}


def build_secrets(rng, n, country, opts):
    notes = ["Configuration excerpt (non-functional example values):"] + v.fake_secrets()
    return "Application configuration", "Deployment notes for the synthetic core banking connector.", [], notes, {"secret": len(v.fake_secrets())}


def build_portfolio(rng, n, country, opts):
    instruments = ["SYNTH Global Equity Fund A", "SYNTH Short Duration Bond B", "SYNTH Real Assets C"]
    rows = [[v.portfolio_id(rng), v.client_id(rng), rng.choice(instruments), str(rng.randint(10, 5000)), v.amount(rng)] for _ in range(n)]
    ctx = "Portfolio valuation statement per client for the private banking review."
    headers = ["Portfolio ID", "Client ID", "Instrument", "Quantity", "Market value"]
    return "Portfolio valuation", ctx, [Section("Holdings", headers, rows)], [], {"portfolio_id": n, "client_id": n}


def build_transactions(rng, n, country, opts):
    rows = [[f"2026-01-{rng.randint(1, 28):02d}", v.synthetic_iban(rng, country), v.synthetic_iban(rng, country), v.amount(rng), v.CURRENCY[country], f"SYN-REF-{rng.randint(0, 999_999):06d}"] for _ in range(n)]
    headers = ["Date", "Debtor IBAN", "Creditor IBAN", "Amount", "Currency", "Reference"]
    return "Transaction list", "Client transaction list for reconciliation.", [Section("Transactions", headers, rows)], [], {"transaction": n, "iban": 2 * n}


def build_hr_salary(rng, n, country, opts):
    rows = [[f"EMP-SYN-{rng.randint(0, 9999):04d}", v.person(rng, country)["name"], rng.choice(["G5", "G6", "G7", "G8"]), v.amount(rng, 60_000, 180_000), v.amount(rng, 0, 50_000), v.CURRENCY[country]] for _ in range(n)]
    headers = ["Employee ID", "Name", "Grade", "Base salary", "Bonus", "Currency"]
    return "Compensation review", "Annual compensation review, HR confidential.", [Section("Employees", headers, rows)], [], {"hr_record": n}


def build_negative(rng, n, country, opts):
    notes = [
        "Facilities update: the third floor meeting rooms will be repainted next week.",
        "Please book rooms on the second floor in the meantime.",
        "The coffee machine maintenance is scheduled for Friday morning.",
    ]
    return "Facilities update", None, [], notes, {}


BUILDERS = {
    "iban": build_iban,
    "iban_invalid": build_iban_invalid,
    "client_id": build_client_id,
    "card_pan": build_card_pan,
    "kyc": build_kyc,
    "aml": build_aml,
    "secrets": build_secrets,
    "portfolio": build_portfolio,
    "transactions": build_transactions,
    "hr_salary": build_hr_salary,
    "negative": build_negative,
}


def build_document(scenario: dict, rng: random.Random) -> tuple[Document, dict]:
    country = scenario["jurisdiction"]
    with_context = scenario.get("context_keywords", True)
    opts = scenario.get("options", {})
    titles, contexts, sections, notes, counts = [], [], [], [], {}
    for item in scenario["data"]:
        builder = BUILDERS[item["category"]]
        title, ctx, secs, nts, cnt = builder(rng, int(item.get("count", 1)), country, opts)
        titles.append(title)
        if ctx:
            contexts.append(ctx)
        sections += secs
        notes += nts
        for key, value in cnt.items():
            counts[key] = counts.get(key, 0) + value

    if not with_context:
        for i, section in enumerate(sections, start=1):
            section.heading = f"Section {i}"
            section.headers = [f"Field {j}" for j in range(1, len(section.headers) + 1)]
        doc = Document(title=f"Document {scenario['id']}", context=None, sections=sections, notes=notes)
    else:
        doc = Document(title=" / ".join(titles), context=" ".join(contexts) or None, sections=sections, notes=notes)
    return doc, counts
