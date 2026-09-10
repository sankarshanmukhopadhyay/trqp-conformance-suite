#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RESULT_MAP = {
    "PASS": "PASS",
    "FAIL": "FAIL",
    "NOT_APPLICABLE": "NOT_APPLICABLE",
    "SKIP": "INDETERMINATE",
    "ERROR": "INDETERMINATE",
    "XFAIL": "INDETERMINATE",
}


def test_set_revision(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(report: dict, *, suite_version: str, protocol_version: str, binding: str,
          test_set_id: str, test_set_revision_value: str,
          reassessment_state: str = "CURRENT", profile_context: dict | None = None) -> dict:
    results = []
    for item in report.get("results", []):
        raw = item.get("result")
        if raw not in RESULT_MAP:
            raise ValueError(f"unsupported CTS result: {raw}")
        result = {
            "test_case_id": item["test_case_id"],
            "result": RESULT_MAP[raw],
            "evidence_ref": f"cts-report.json#test_case_id={item['test_case_id']}",
        }
        if item.get("reason"):
            result["reason"] = item["reason"]
        results.append(result)

    evidence = {
        "schema_version": "1.0",
        "producer": "trqp-conformance-suite",
        "suite_version": suite_version,
        "test_set": {"id": test_set_id, "revision": test_set_revision_value},
        "protocol": {"id": "trqp", "version": protocol_version, "binding": binding},
        "run": {"id": report["run_id"], "generated_at": report["generated_at"]},
        "target": {"id": report["target_id"]},
        "results": results,
        "reassessment": {"state": reassessment_state},
    }
    if profile_context:
        evidence["profile_context"] = dict(profile_context)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--protocol-version", required=True)
    parser.add_argument("--binding", default="https-json")
    parser.add_argument("--test-set", type=Path, default=Path("tests/core_tests.yaml"))
    parser.add_argument("--test-set-id", default="core-tests")
    parser.add_argument("--reassessment-state", choices=["CURRENT", "REASSESS_REQUIRED", "INVALID"], default="CURRENT")
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    suite_version = Path("VERSION").read_text(encoding="utf-8").strip()
    evidence = build(
        report,
        suite_version=suite_version,
        protocol_version=args.protocol_version,
        binding=args.binding,
        test_set_id=args.test_set_id,
        test_set_revision_value=test_set_revision(args.test_set),
        reassessment_state=args.reassessment_state,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
