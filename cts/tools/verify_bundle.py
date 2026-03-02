#!/usr/bin/env python3
"""Verify a CTS report directory / evidence bundle.

Checks:
- Required files exist
- checksums.json includes bundle.zip and matches its sha256
- bundle_descriptor.json includes an entry for bundle.zip and matches sha256
- (optional) validate manifest.json/verdicts.json/run.json are valid JSON

Stdlib-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED_FILES = [
    "manifest.json",
    "verdicts.json",
    "run.json",
    "checksums.json",
    "bundle_descriptor.json",
    "bundle.zip",
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_json(p: Path) -> object:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(prog="cts-verify-bundle")
    ap.add_argument("--dir", required=True, help="Report directory")
    args = ap.parse_args()

    d = Path(args.dir)
    if not d.exists() or not d.is_dir():
        raise SystemExit(f"Not a directory: {d}")

    errors: list[str] = []

    for fn in REQUIRED_FILES:
        if not (d / fn).exists():
            errors.append(f"missing required file: {fn}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 2

    # JSON sanity
    for fn in ["manifest.json", "verdicts.json", "run.json", "checksums.json", "bundle_descriptor.json"]:
        try:
            _read_json(d / fn)
        except Exception as e:
            errors.append(f"invalid json in {fn}: {e}")

    bundle_hash = sha256(d / "bundle.zip")

    # checksums.json
    try:
        checks = _read_json(d / "checksums.json")
        entries = {e.get("path"): e.get("sha256") for e in checks.get("entries", []) if isinstance(e, dict)}
        if entries.get("bundle.zip") != bundle_hash:
            errors.append("checksums.json sha256 mismatch for bundle.zip")
    except Exception as e:
        errors.append(f"checksums.json parse error: {e}")

    # bundle_descriptor.json
    try:
        desc = _read_json(d / "bundle_descriptor.json")
        idx = [e for e in desc.get("artifact_index", []) if isinstance(e, dict) and e.get("path") == "bundle.zip"]
        if not idx:
            errors.append("bundle_descriptor.json missing artifact_index entry for bundle.zip")
        else:
            if idx[-1].get("sha256") != bundle_hash:
                errors.append("bundle_descriptor.json sha256 mismatch for bundle.zip")
    except Exception as e:
        errors.append(f"bundle_descriptor.json parse error: {e}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 2

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
