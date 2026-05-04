#!/usr/bin/env python3
"""Generate an adoption-facing interop evidence matrix from a CTS report."""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    report = json.loads(Path(args.report).read_text())
    profile = report.get("profile_id", "unknown")
    summary = report.get("summary", {})
    rows = [
        {
            "requirement": "Protocol conformance",
            "test": "CTS profile execution",
            "result": "pass" if summary.get("FAIL", 0) == 0 and summary.get("ERROR", 0) == 0 else "fail",
            "evidence": "cts-report.json",
            "consumer_relevance": "Reduces risk that registry responses are non-interoperable or inconsistent.",
        },
        {
            "requirement": "Evidence completeness",
            "test": "Evidence completeness metric",
            "result": str(summary.get("evidence_completeness", "unknown")),
            "evidence": "cts-report.json summary",
            "consumer_relevance": "Shows whether the conformance claim is backed by reviewable artifacts.",
        },
        {
            "requirement": "Coverage",
            "test": "Coverage index metric",
            "result": str(summary.get("coverage_index", "unknown")),
            "evidence": "cts-report.json summary",
            "consumer_relevance": "Shows whether the evaluated surface is broad enough for reliance.",
        },
    ]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".json":
        out.write_text(json.dumps({"profile_id": profile, "matrix": rows}, indent=2) + "\n")
    else:
        lines = [
            "# Interop Evidence Matrix",
            "",
            f"Profile: `{profile}`",
            "",
            "| Requirement | Test | Result | Evidence | Consumer/relying-party relevance |",
            "|---|---|---|---|---|",
        ]
        for r in rows:
            lines.append(f"| {r['requirement']} | {r['test']} | {r['result']} | {r['evidence']} | {r['consumer_relevance']} |")
        out.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
