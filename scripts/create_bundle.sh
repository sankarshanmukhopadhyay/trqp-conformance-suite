#!/usr/bin/env bash
set -euo pipefail

# Create a bundle.zip inside a report directory if it does not already exist.
# Usage: ./scripts/create_bundle.sh reports/ci_baseline

REPORT_DIR="${1:?report dir required}"
cd "$REPORT_DIR"

if [ -f bundle.zip ]; then
  echo "bundle.zip already present in $REPORT_DIR"
  exit 0
fi

# Prefer zip if available
if command -v zip >/dev/null 2>&1; then
  # Exclude any existing zip outputs to avoid recursion
  zip -r bundle.zip . -x "bundle.zip"
  echo "Created bundle.zip in $REPORT_DIR"
  exit 0
fi

# Fallback to python
python - <<'PY'
import os, zipfile
root = "."
with zipfile.ZipFile("bundle.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn == "bundle.zip":
                continue
            p = os.path.join(dirpath, fn)
            arc = os.path.relpath(p, root)
            z.write(p, arcname=arc)
print("Created bundle.zip")
PY
