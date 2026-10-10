"""Command line interface: python -m dlpgen <command>."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dlpgen import __version__
from dlpgen.generate import clean, generate
from dlpgen.validate import validate_output, validate_repo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dlpgen", description="Synthetic banking files for DLP testing.")
    parser.add_argument("--version", action="version", version=f"dlpgen {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate", help="generate the corpus from a config file")
    p_gen.add_argument("--config", required=True, type=Path)
    p_gen.add_argument("--output", type=Path, default=None)

    p_out = sub.add_parser("validate-output", help="check hashes and markers of a generated corpus")
    p_out.add_argument("--manifest", required=True, type=Path)

    p_repo = sub.add_parser("validate-repo", help="scan versioned text files for real-looking sensitive data")
    p_repo.add_argument("--root", default=Path("."), type=Path)

    p_clean = sub.add_parser("clean", help="delete a generated corpus")
    p_clean.add_argument("--output", default=Path("output"), type=Path)

    args = parser.parse_args(argv)

    if args.command == "generate":
        manifest = generate(args.config, args.output)
        print(f"Generated corpus. Manifest: {manifest}")
        return 0
    if args.command == "validate-output":
        errors = validate_output(args.manifest)
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print("validate-output: OK" if not errors else f"validate-output: {len(errors)} error(s)")
        return 1 if errors else 0
    if args.command == "validate-repo":
        findings = validate_repo(args.root)
        for finding in findings:
            print(f"FINDING {finding}", file=sys.stderr)
        print("validate-repo: OK" if not findings else f"validate-repo: {len(findings)} finding(s)")
        return 1 if findings else 0
    if args.command == "clean":
        removed = clean(args.output)
        print("Removed." if removed else "Nothing to remove.")
        return 0
    return 2
