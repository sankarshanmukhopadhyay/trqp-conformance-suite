#!/usr/bin/env bash
set -euo pipefail

# Create a deterministic bundle.zip inside a report directory if it does not already exist.
# Usage: ./scripts/create_bundle.sh reports/ci_baseline

REPORT_DIR="${1:?report dir required}"

if [ -f "${REPORT_DIR}/bundle.zip" ]; then
  echo "bundle.zip already present in ${REPORT_DIR}"
  exit 0
fi

# Deterministic bundling (stable ordering + normalized timestamps/perms)
python -m cts.tools.deterministic_zip --dir "${REPORT_DIR}" --out "${REPORT_DIR}/bundle.zip"

python - <<'PY'
import json, hashlib
from pathlib import Path
import sys

report_dir = Path(sys.argv[1])

def sha256(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

out = report_dir
zip_p = out/"bundle.zip"
if not zip_p.exists():
    raise SystemExit(1)

desc_p = out/"bundle_descriptor.json"
checks_p = out/"checksums.json"

desc = json.loads(desc_p.read_text(encoding="utf-8")) if desc_p.exists() else {"bundle_version":"0.1.0","artifacts":{},"artifact_index":[]}
desc.setdefault("artifacts", {})
desc["artifacts"]["bundle_zip"] = "bundle.zip"

idx = desc.setdefault("artifact_index", [])
idx = [e for e in idx if e.get("kind") != "cts_bundle_zip"]
idx.append({
    "kind": "cts_bundle_zip",
    "artifact_kind": "conformance_evidence_bundle_zip",
    "path": "bundle.zip",
    "produced_by": "trqp-cts",
    "sha256": sha256(zip_p),
    "media_type": "application/zip",
})
desc["artifact_index"] = idx
desc_p.write_text(json.dumps(desc, indent=2) + "\n", encoding="utf-8")

checks = json.loads(checks_p.read_text(encoding="utf-8")) if checks_p.exists() else {"checksums_version":"0.1.0","algorithm":"sha256","entries":[]}
entries = {e["path"]: e["sha256"] for e in checks.get("entries", []) if isinstance(e, dict) and "path" in e and "sha256" in e}
entries["bundle.zip"] = sha256(zip_p)
checks["entries"] = [{"path": p, "sha256": h} for p,h in sorted(entries.items())]
checks_p.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")
print("Updated bundle_descriptor.json + checksums.json for bundle.zip")
PY
"${REPORT_DIR}"
