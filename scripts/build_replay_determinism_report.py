#!/usr/bin/env python3
"""Build an auditable determinism report from a source CTS run and its replay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import validate

from cts.determinism import classify_differences, diff_documents, semantic_sha256, summarize_differences

ROOT = Path(__file__).resolve().parent.parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_case_projection(source_dir: Path, replay_report: dict) -> tuple[dict, dict]:
    original_verdicts = {
        item["test_case_id"]: item
        for item in load_json(source_dir / "verdicts.json")
    }
    replay_verdicts = {
        item["test_case_id"]: item
        for item in replay_report.get("verdicts", [])
    }

    original_cases = {}
    replay_cases = {}
    for case_path in sorted((source_dir / "cases").glob("*.json")):
        tc_id = case_path.stem
        case = load_json(case_path)
        response = case.get("response", {})
        common = {
            "request": {
                "method": case.get("request", {}).get("method"),
                "path": case.get("request", {}).get("path"),
                "body": case.get("request", {}).get("body"),
            },
            "response": {
                "status": response.get("status"),
                "json": response.get("json"),
                "text": response.get("text", ""),
            },
            "elapsed_ms": case.get("elapsed_ms", 0),
        }
        original_cases[tc_id] = {
            **common,
            "assertions": case.get("assertions", []),
            "result": original_verdicts.get(tc_id, {}).get("result"),
        }
        replay_cases[tc_id] = {
            **common,
            "elapsed_ms": 0,
            "assertions": replay_verdicts.get(tc_id, {}).get("assertions", case.get("assertions", [])),
            "result": replay_verdicts.get(tc_id, {}).get("result"),
        }
    return original_cases, replay_cases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--replay-report", required=True, type=Path)
    parser.add_argument("--policy", default=ROOT / "policies/replay-determinism.v1.json", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    source_run = load_json(args.source / "run.json")
    replay_report = load_json(args.replay_report)
    policy = load_json(args.policy)

    original_cases, replay_cases = build_case_projection(args.source, replay_report)
    original = {
        "run": {
            "test_run_id": source_run.get("test_run_id"),
            "generated_at": source_run.get("started_at"),
            "started_at": source_run.get("started_at"),
            "ended_at": source_run.get("ended_at"),
            "out_dir_label": source_run.get("out_dir_label"),
            "profile_id": source_run.get("profile_id"),
            "target_id": source_run.get("target_id"),
            "tool": source_run.get("tool"),
        },
        "cases": original_cases,
    }
    replay = {
        "run": {
            "test_run_id": replay_report.get("replay_of_run_id"),
            "replay_run_id": replay_report.get("replay_run_id"),
            "generated_at": replay_report.get("generated_at"),
            "started_at": replay_report.get("generated_at"),
            "ended_at": replay_report.get("generated_at"),
            "out_dir_label": args.out.parent.name,
            "profile_id": replay_report.get("profile_id"),
            "target_id": source_run.get("target_id"),
            "tool": source_run.get("tool"),
        },
        "cases": replay_cases,
    }

    classified = classify_differences(diff_documents(original, replay), policy)
    summary = summarize_differences(classified)
    prohibited = summary["prohibited_difference_count"]

    report = {
        "report_version": "1.0.0",
        "policy": {
            "id": policy["policy_id"],
            "version": policy["policy_version"],
            "sha256": sha256_file(args.policy),
        },
        "source": {
            "run_id": source_run.get("test_run_id"),
            "semantic_sha256": semantic_sha256(original),
        },
        "replay": {
            "run_id": replay_report.get("replay_run_id"),
            "semantic_sha256": semantic_sha256(replay),
        },
        "deterministic": prohibited == 0,
        "summary": summary,
        "differences": classified,
    }

    schema = load_json(ROOT / "schemas/evidence/replay-determinism-report.schema.json")
    validate(instance=report, schema=schema)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Determinism {'PASSED' if report['deterministic'] else 'FAILED'}: {summary}")
    return 0 if report["deterministic"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
