#!/usr/bin/env python3
"""Validate the experimental TRQP v3 candidate vector corpus.

This is deliberately dependency-free so that candidate semantic evidence can be
replayed in repository CI without requiring a live SUT. It validates the pinned
candidate source, complete requirement coverage, and fail-closed outcomes.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PIN_PATH = ROOT / "experimental" / "trqp-v3" / "source-pin.json"
VECTORS_PATH = ROOT / "experimental" / "trqp-v3" / "vectors.json"

CANDIDATE_SHA = "532a570ed8b7b468b7a317030077577b9859c14f"
AUTHORITY_STATUS = "DOWNSTREAM_EXPERIMENTAL_NOT_ADOPTED"

REQUIRED_REQUIREMENTS = {
    "TRQP3-PROP-001", "TRQP3-PROP-002",
    "TRQP3-MAT-001", "TRQP3-MAT-002", "TRQP3-MAT-003",
    "TRQP3-CTX-001",
    "TRQP3-LIFE-001", "TRQP3-LIFE-002", "TRQP3-LIFE-003",
    "TRQP3-EVID-001", "TRQP3-EVID-002", "TRQP3-EVID-003",
    "TRQP3-DEC-001", "TRQP3-DEC-002",
    "TRQP3-REQ-001", "TRQP3-EVAL-001", "TRQP3-RESP-001",
    "TRQP3-NEG-001", "TRQP3-NEG-002", "TRQP3-BIND-001",
    "TRQP3-DISC-001", "TRQP3-DISC-002",
    "TRQP3-PROF-001", "TRQP3-PROF-002",
    "TRQP3-REC-001", "TRQP3-REC-002",
    "TRQP3-ERR-001", "TRQP3-SEC-001", "TRQP3-SEC-002",
    "TRQP3-PRIV-001", "TRQP3-AUD-001", "TRQP3-COMP-001",
}

BASE_INPUT: dict[str, Any] = {
    "proposition_exact": True,
    "decision_critical_preserved": True,
    "principal_valid": True,
    "material_required": True,
    "material_matches": True,
    "material_state": "active",
    "critical_supported": True,
    "critical_declaration_valid": True,
    "profile_conflict": False,
    "profile_weakens_core": False,
    "historical": False,
    "historical_evidence_sufficient": True,
    "historical_material_state": "active",
    "evidence_authoritative": True,
    "evidence_scope_ok": True,
    "evidence_complete": True,
    "evidence_fresh": True,
    "evidence_temporal": True,
    "evidence_provenance": True,
    "evidence_conflict": False,
    "absence_claimed": False,
    "absence_authoritative": False,
    "transport_ok": True,
    "requested_version": "v3",
    "negotiated_version": "v3",
    "legacy_fallback": False,
    "processing_contract_established": True,
    "binding_changes_semantics": False,
    "discovery_used_as_authority": False,
    "capability_metadata_valid": True,
    "recognition_used_as_authorization": False,
    "recognition_transitive_without_authority": False,
    "adversarial": [],
    "privacy_dropped_critical": False,
    "audit_reconstructable": True,
    "applicable": True,
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def evaluate(overrides: dict[str, Any]) -> dict[str, str]:
    state = dict(BASE_INPUT)
    unknown = set(overrides) - set(BASE_INPUT)
    if unknown:
        raise ValueError(f"unknown vector input fields: {sorted(unknown)}")
    state.update(overrides)

    if not state["applicable"]:
        return {"semantic_decision": "not_applicable", "processing": "accept"}

    fail_closed = (
        not state["decision_critical_preserved"]
        or not state["critical_supported"]
        or not state["critical_declaration_valid"]
        or state["profile_conflict"]
        or state["profile_weakens_core"]
        or not state["proposition_exact"]
        or state["privacy_dropped_critical"]
        or state["binding_changes_semantics"]
        or state["discovery_used_as_authority"]
        or state["recognition_used_as_authorization"]
        or not state["processing_contract_established"]
        or (state["requested_version"] == "v3" and state["negotiated_version"] != "v3")
        or state["legacy_fallback"]
        or not state["capability_metadata_valid"]
        or not state["audit_reconstructable"]
        or bool(state["adversarial"])
        or not state["transport_ok"]
    )
    if fail_closed:
        return {"semantic_decision": "indeterminate", "processing": "reject"}

    if state["recognition_transitive_without_authority"]:
        return {"semantic_decision": "negative", "processing": "accept"}

    if state["material_required"]:
        if not state["material_matches"]:
            return {"semantic_decision": "negative", "processing": "accept"}
        if state["historical"] and not state["historical_evidence_sufficient"]:
            return {"semantic_decision": "indeterminate", "processing": "accept"}
        material_state = (
            state["historical_material_state"]
            if state["historical"]
            else state["material_state"]
        )
        if material_state in {"revoked", "expired", "superseded"}:
            return {"semantic_decision": "negative", "processing": "accept"}

    insufficient_evidence = (
        not state["evidence_authoritative"]
        or not state["evidence_scope_ok"]
        or not state["evidence_complete"]
        or not state["evidence_fresh"]
        or not state["evidence_temporal"]
        or not state["evidence_provenance"]
        or state["evidence_conflict"]
    )
    if state["absence_claimed"]:
        if state["absence_authoritative"] and not insufficient_evidence:
            return {"semantic_decision": "negative", "processing": "accept"}
        return {"semantic_decision": "indeterminate", "processing": "accept"}

    if insufficient_evidence:
        return {"semantic_decision": "indeterminate", "processing": "accept"}

    return {"semantic_decision": "positive", "processing": "accept"}


def validate() -> dict[str, Any]:
    pin = load_json(PIN_PATH)
    corpus = load_json(VECTORS_PATH)

    if pin.get("commit") != CANDIDATE_SHA:
        raise AssertionError("candidate source pin moved without explicit reassessment")
    if pin.get("authority_status") != AUTHORITY_STATUS:
        raise AssertionError("candidate authority boundary is missing or changed")
    if corpus.get("candidate_commit") != CANDIDATE_SHA:
        raise AssertionError("vector corpus is not bound to the pinned candidate")
    if corpus.get("authority_status") != AUTHORITY_STATUS:
        raise AssertionError("vector corpus authority status is invalid")

    vectors = corpus.get("vectors")
    if not isinstance(vectors, list) or not vectors:
        raise AssertionError("candidate vector corpus must be a non-empty list")

    ids: set[str] = set()
    covered: set[str] = set()
    results: list[dict[str, Any]] = []

    for vector in vectors:
        vector_id = vector.get("id")
        if not vector_id or vector_id in ids:
            raise AssertionError(f"duplicate or missing vector id: {vector_id!r}")
        ids.add(vector_id)

        requirements = set(vector.get("requirements") or [])
        if not requirements:
            raise AssertionError(f"{vector_id}: no requirement IDs")
        unknown_requirements = requirements - REQUIRED_REQUIREMENTS
        if unknown_requirements:
            raise AssertionError(
                f"{vector_id}: unknown requirement IDs {sorted(unknown_requirements)}"
            )
        covered.update(requirements)

        actual = evaluate(vector.get("overrides") or {})
        expected = vector.get("expected")
        if actual != expected:
            raise AssertionError(f"{vector_id}: expected {expected}, got {actual}")
        results.append({
            "id": vector_id,
            "requirements": sorted(requirements),
            "result": "PASS",
            "semantic_decision": actual["semantic_decision"],
            "processing": actual["processing"],
        })

    missing = REQUIRED_REQUIREMENTS - covered
    if missing:
        raise AssertionError(
            f"candidate requirements without executable vectors: {sorted(missing)}"
        )

    return {
        "candidate_commit": CANDIDATE_SHA,
        "authority_status": AUTHORITY_STATUS,
        "requirement_count": len(REQUIRED_REQUIREMENTS),
        "vector_count": len(vectors),
        "covered_requirements": sorted(covered),
        "results": results,
    }


def main() -> int:
    report = validate()
    print(json.dumps({
        "candidate_commit": report["candidate_commit"],
        "authority_status": report["authority_status"],
        "requirement_count": report["requirement_count"],
        "vector_count": report["vector_count"],
        "status": "PASS",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
