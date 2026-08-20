#!/usr/bin/env python3
"""Verify that a CTS replay reproduced the original semantic verdicts.

A replay can legitimately reproduce FAIL verdicts from the source run. Those
FAIL results are conformance evidence, not replay drift. Determinism fails only
when the replay changes a verdict or cannot map a captured case to the current
suite.
"""

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_replay_determinism.py <replay-report.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"Replay determinism FAILED: report not found: {path}", file=sys.stderr)
        return 2

    report = json.loads(path.read_text(encoding="utf-8"))
    summary = report.get("summary") or {}
    diffs = report.get("verdict_diffs") or []
    stale = int(summary.get("STALE", 0) or 0)

    if len(diffs) != int(summary.get("verdict_diffs", len(diffs)) or 0):
        print("Replay determinism FAILED: report summary disagrees with verdict_diffs", file=sys.stderr)
        return 2

    if diffs or stale:
        print(
            f"Replay determinism FAILED: {len(diffs)} verdict drift(s), {stale} stale case(s).",
            file=sys.stderr,
        )
        for diff in diffs:
            print(
                f"- {diff.get('test_case_id')}: {diff.get('original_result')} -> {diff.get('replay_result')}",
                file=sys.stderr,
            )
        return 1

    reproduced_failures = int(summary.get("FAIL", 0) or 0)
    print(
        "Replay determinism PASSED: 0 verdict drifts, 0 stale cases; "
        f"{reproduced_failures} source FAIL verdict(s) reproduced without semantic change."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
