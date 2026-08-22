#!/usr/bin/env python3
"""Attach replay determinism evidence to an existing CTS evidence directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir
    report_dest = run_dir / "determinism-report.json"
    policy_dest = run_dir / "replay-determinism-policy.json"
    shutil.copy2(args.report, report_dest)
    shutil.copy2(args.policy, policy_dest)

    descriptor_path = run_dir / "bundle_descriptor.json"
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    descriptor.setdefault("artifacts", {})["determinism_report"] = report_dest.name
    descriptor["artifacts"]["determinism_policy"] = policy_dest.name
    index = [
        item for item in descriptor.setdefault("artifact_index", [])
        if item.get("kind") not in {"cts_replay_determinism_report", "cts_replay_determinism_policy", "cts_bundle_zip"}
    ]
    index.extend([
        {
            "kind": "cts_replay_determinism_report",
            "artifact_kind": "conformance_replay_determinism_report",
            "path": report_dest.name,
            "produced_by": "trqp-cts",
            "sha256": sha256(report_dest),
            "media_type": "application/json"
        },
        {
            "kind": "cts_replay_determinism_policy",
            "artifact_kind": "conformance_replay_determinism_policy",
            "path": policy_dest.name,
            "produced_by": "trqp-cts",
            "sha256": sha256(policy_dest),
            "media_type": "application/json"
        }
    ])
    descriptor["artifact_index"] = index
    descriptor_path.write_text(json.dumps(descriptor, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksums_path = run_dir / "checksums.json"
    checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
    entries = {
        item["path"]: item["sha256"]
        for item in checksums.get("entries", [])
        if isinstance(item, dict) and item.get("path") and item.get("sha256") and item.get("path") != "bundle.zip"
    }
    entries[report_dest.name] = sha256(report_dest)
    entries[policy_dest.name] = sha256(policy_dest)
    entries[descriptor_path.name] = sha256(descriptor_path)
    checksums["entries"] = [{"path": p, "sha256": entries[p]} for p in sorted(entries)]
    checksums_path.write_text(json.dumps(checksums, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    bundle = run_dir / "bundle.zip"
    if bundle.exists():
        bundle.unlink()
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(run_dir.rglob("*")):
            if path.is_file() and path != bundle:
                archive.write(path, arcname=str(path.relative_to(run_dir)))

    bundle_hash = sha256(bundle)
    descriptor = json.loads(descriptor_path.read_text(encoding="utf-8"))
    descriptor.setdefault("artifacts", {})["bundle_zip"] = "bundle.zip"
    descriptor["artifact_index"].append({
        "kind": "cts_bundle_zip",
        "artifact_kind": "conformance_evidence_bundle_zip",
        "path": "bundle.zip",
        "produced_by": "trqp-cts",
        "sha256": bundle_hash,
        "media_type": "application/zip"
    })
    descriptor_path.write_text(json.dumps(descriptor, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksums = json.loads(checksums_path.read_text(encoding="utf-8"))
    entries = {item["path"]: item["sha256"] for item in checksums.get("entries", [])}
    entries["bundle.zip"] = bundle_hash
    checksums["entries"] = [{"path": p, "sha256": entries[p]} for p in sorted(entries)]
    checksums_path.write_text(json.dumps(checksums, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Attached determinism evidence to {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
