"""Create labels, milestones and issues from .github/labels.yml and backlog/initial-backlog.csv.

Uses the GitHub CLI (`gh`), already authenticated. Dry run by default: prints the commands.

    python automation/bootstrap_github.py --repo <owner>/<repo>            # dry run
    python automation/bootstrap_github.py --repo <owner>/<repo> --apply    # execute

Run it once on an empty repository so that issue numbers match the roadmap (#1 to #28).
Existing labels are updated, existing milestones and issues (same title) are skipped.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], apply: bool) -> str:
    print(("RUN  " if apply else "DRY  ") + " ".join(cmd))
    if not apply:
        return ""
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def existing_milestones(repo: str) -> set[str]:
    out = subprocess.run(
        ["gh", "api", f"repos/{repo}/milestones?state=all&per_page=100"], check=True, capture_output=True, text=True
    ).stdout
    return {m["title"] for m in json.loads(out)}


def existing_issue_titles(repo: str) -> set[str]:
    out = subprocess.run(
        ["gh", "issue", "list", "--repo", repo, "--state", "all", "--limit", "1000", "--json", "title"],
        check=True, capture_output=True, text=True,
    ).stdout
    return {i["title"] for i in json.loads(out)}


def issue_body(row: dict) -> str:
    depends = ", ".join(f"#{d}" if d.isdigit() else d for d in row["depends_on"].split(";") if d) or "none"
    return (
        f"{row['description']}\n\n"
        f"**Acceptance criteria**\n\n{row['acceptance_criteria']}\n\n"
        f"**Depends on:** {depends}\n\n"
        f"_Backlog item {row['id']} (backlog/initial-backlog.csv). Synthetic data only._"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", required=True, help="owner/name")
    parser.add_argument("--apply", action="store_true", help="execute instead of printing")
    args = parser.parse_args()

    labels = yaml.safe_load((ROOT / ".github" / "labels.yml").read_text(encoding="utf-8"))
    with (ROOT / "backlog" / "initial-backlog.csv").open(encoding="utf-8") as handle:
        backlog = sorted(csv.DictReader(handle), key=lambda r: int(r["id"]))

    for label in labels:
        run(["gh", "label", "create", label["name"], "--repo", args.repo, "--color", label["color"],
             "--description", label["description"], "--force"], args.apply)

    have_ms = existing_milestones(args.repo) if args.apply else set()
    for milestone in sorted({row["milestone"] for row in backlog}, key=lambda m: [int(x) for x in m[1:].split(".")]):
        if milestone not in have_ms:
            run(["gh", "api", f"repos/{args.repo}/milestones", "-f", f"title={milestone}"], args.apply)

    have_issues = existing_issue_titles(args.repo) if args.apply else set()
    for row in backlog:
        if row["title"] in have_issues:
            print(f"SKIP existing issue: {row['title']}")
            continue
        cmd = ["gh", "issue", "create", "--repo", args.repo, "--title", row["title"], "--body", issue_body(row),
               "--milestone", row["milestone"]]
        for label in filter(None, row["labels"].split(";")):
            cmd += ["--label", label]
        cmd += ["--label", row["priority"] if row["priority"].startswith("priority/") else f"priority/{row['priority']}"]
        run(cmd, args.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
