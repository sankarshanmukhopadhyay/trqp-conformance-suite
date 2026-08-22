#!/usr/bin/env python3
"""Verify CTS replay determinism evidence."""

import json
import sys
from pathlib import Path


def verify_v1(report: dict) -> int:
    summary = report.get("summary") or {}
    prohibited = int(summary.get("prohibited_difference_count", 0) or 0)
    permitted = int(summary.get("permitted_difference_count", 0) or 0)
    differences = report.get("differences") or []

    if len(differences) != int(summary.get("difference_count", len(differences)) or 0):
        print("Replay determinism FAILED: summary disagrees with differences", file=sys.stderr)
        return 2
    if prohibited != sum(1 for d in differences if not d.get("permitted", False)):
        print("Replay determinism FAILED: prohibited difference count is inconsistent", file=sys.stderr)
        return 2
    if report.get("deterministic") is not (prohibited == 0):
        print("Replay determinism FAILED: deterministic flag is inconsistent", file=sys.stderr)
        return 2

    policy = report.get("policy") or {}
    if not policy.get("id") or not policy.get("version") or not policy.get("sha256"):
        print("Replay determinism FAILED: policy provenance is incomplete", file=sys.stderr)
        return 2

    if prohibited:
        print(f"Replay determinism FAILED: {prohibited} prohibited semantic difference(s).", file=sys.stderr)
        for diff in differences:
            if not diff.get("permitted", False):
                print(f"- {diff.get('pointer')}: {diff.get('original')!r} -> {diff.get('replay')!r}", file=sys.stderr)
        return 1

    print(
        "Replay determinism PASSED: "
        f"0 prohibited semantic differences; {permitted} permitted volatile difference(s); "
        f"policy {policy.get('id')}@{policy.get('version')}."
    )
    return 0


def verify_legacy(report: dict) -> int:
    summary = report.get("summary") or {}
    diffs = report.get("verdict_diffs") or []
    stale = int(summary.get("STALE", 0) or 0)
    if len(diffs) != int(summary.get("verdict_diffs", len(diffs)) or 0):
        print("Replay determinism FAILED: report summary disagrees with verdict_diffs", file=sys.stderr)
        return 2
    if diffs or stale:
        print(f"Replay determinism FAILED: {len(diffs)} verdict drift(s), {stale} stale case(s).", file=sys.stderr)
        return 1
    print("Replay determinism PASSED (legacy verdict-only report).")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_replay_determinism.py <determinism-report.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Replay determinism FAILED: report not found: {path}", file=sys.stderr)
        return 2
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("report_version") == "1.0.0":
        return verify_v1(report)
    return verify_legacy(report)


if __name__ == "__main__":
    raise SystemExit(main())
