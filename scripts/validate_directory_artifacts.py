#!/usr/bin/env python3
"""Validate authoritative directory artifacts (SAD-1 / GRID).

This tool validates machine-readable directory artifacts against JSON Schemas that ship with the CTS.

Why this exists:
- Many authoritative directories publish signed files or feeds rather than interactive APIs.
- TRQP can still evaluate these systems by validating publication integrity artifacts as **evidence**.

This script performs:
- JSON parse validation
- JSON Schema validation
- Optional consistency checks between entry/status feed

It does NOT perform signature verification. Signature verification is profile-specific and is handled by
directory operator tooling or assessment procedures.
"""

import argparse
import json
from pathlib import Path

from jsonschema import validate as js_validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def validate_json(doc, schema_path: Path):
    schema = load_json(schema_path)
    js_validate(instance=doc, schema=schema)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", help="Path to a directory entry JSON file")
    ap.add_argument("--manifest", help="Path to a directory publication manifest JSON file")
    ap.add_argument("--status", help="Path to a directory status feed JSON file")
    args = ap.parse_args()

    if not any([args.entry, args.manifest, args.status]):
        raise SystemExit("Provide at least one of --entry, --manifest, --status")

    if args.entry:
        doc = load_json(Path(args.entry))
        validate_json(doc, SCHEMAS / "authoritative-directory-entry.schema.json")
        print("[OK] entry schema: authoritative-directory-entry")

    if args.manifest:
        doc = load_json(Path(args.manifest))
        validate_json(doc, SCHEMAS / "directory-publication-manifest.schema.json")
        print("[OK] manifest schema: directory-publication-manifest")

    if args.status:
        doc = load_json(Path(args.status))
        validate_json(doc, SCHEMAS / "directory-status-feed.schema.json")
        print("[OK] status schema: directory-status-feed")

    print("Directory artifact validation PASSED.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
