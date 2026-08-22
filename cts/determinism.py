"""Deterministic replay comparison helpers for TRQP CTS."""

from __future__ import annotations

import fnmatch
import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Serialize JSON-compatible data using a stable representation."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def semantic_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _escape_pointer_token(token: str) -> str:
    return token.replace("~", "~0").replace("/", "~1")


def diff_documents(original: Any, replay: Any, pointer: str = "") -> list[dict[str, Any]]:
    """Return deterministic JSON-Pointer differences between two documents."""
    diffs: list[dict[str, Any]] = []
    if type(original) is not type(replay):
        return [{"pointer": pointer or "/", "original": original, "replay": replay}]

    if isinstance(original, dict):
        for key in sorted(set(original) | set(replay)):
            child = f"{pointer}/{_escape_pointer_token(str(key))}"
            if key not in original:
                diffs.append({"pointer": child, "original": None, "replay": replay[key]})
            elif key not in replay:
                diffs.append({"pointer": child, "original": original[key], "replay": None})
            else:
                diffs.extend(diff_documents(original[key], replay[key], child))
        return diffs

    if isinstance(original, list):
        length = max(len(original), len(replay))
        for idx in range(length):
            child = f"{pointer}/{idx}"
            if idx >= len(original):
                diffs.append({"pointer": child, "original": None, "replay": replay[idx]})
            elif idx >= len(replay):
                diffs.append({"pointer": child, "original": original[idx], "replay": None})
            else:
                diffs.extend(diff_documents(original[idx], replay[idx], child))
        return diffs

    if original != replay:
        diffs.append({"pointer": pointer or "/", "original": original, "replay": replay})
    return diffs


def classify_differences(diffs: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    allowed_patterns = policy.get("allowed_difference_pointers", [])
    classified = []
    for diff in diffs:
        pointer = diff["pointer"]
        allowed = any(fnmatch.fnmatchcase(pointer, pattern) for pattern in allowed_patterns)
        classified.append({
            **diff,
            "classification": "volatile" if allowed else "semantic",
            "permitted": allowed,
        })
    return classified


def summarize_differences(classified: list[dict[str, Any]]) -> dict[str, int]:
    permitted = sum(1 for d in classified if d["permitted"])
    prohibited = len(classified) - permitted
    return {
        "difference_count": len(classified),
        "permitted_difference_count": permitted,
        "prohibited_difference_count": prohibited,
    }
