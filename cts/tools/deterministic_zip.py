#!/usr/bin/env python3
"""Create a deterministic ZIP bundle for a CTS report directory.

Design goals:
- Same input files => identical ZIP bytes (stable ordering + normalized timestamps/perms).
- Stdlib-only.

Usage:
  python -m cts.tools.deterministic_zip --dir reports/ci_baseline --out bundle.zip
"""

from __future__ import annotations

import argparse
import os
import stat
import zipfile
from pathlib import Path

FIXED_ZIP_DT = (1980, 1, 1, 0, 0, 0)  # earliest DOS time supported by zip


def _iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            if rel == "bundle.zip":
                continue
            files.append(p)
    # Stable ordering: path string sort
    files.sort(key=lambda p: p.relative_to(root).as_posix())
    return files


def make_zip(root: Path, out_zip: Path) -> None:
    root = root.resolve()
    out_zip = out_zip.resolve()

    tmp = out_zip.with_suffix(out_zip.suffix + ".tmp")
    if tmp.exists():
        tmp.unlink()

    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in _iter_files(root):
            arcname = p.relative_to(root).as_posix()

            zi = zipfile.ZipInfo(filename=arcname, date_time=FIXED_ZIP_DT)
            # Normalize permissions: regular file 0644
            zi.external_attr = (stat.S_IFREG | 0o644) << 16
            zi.compress_type = zipfile.ZIP_DEFLATED

            with p.open("rb") as f:
                data = f.read()
            zf.writestr(zi, data)

    tmp.replace(out_zip)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="Report directory to bundle")
    ap.add_argument("--out", default="bundle.zip", help="Output zip path (default: bundle.zip)")
    args = ap.parse_args()

    root = Path(args.dir)
    out_zip = Path(args.out)
    if out_zip.is_dir():
        out_zip = out_zip / "bundle.zip"
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Report directory not found: {root}")

    make_zip(root, out_zip)
    print(str(out_zip))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
