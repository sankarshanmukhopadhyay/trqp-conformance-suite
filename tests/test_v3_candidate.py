import json
import unittest
from pathlib import Path

from scripts.validate_v3_candidate import (
    CANDIDATE_SHA,
    REQUIRED_REQUIREMENTS,
    evaluate,
    validate,
)


class CandidateV3EvidenceTests(unittest.TestCase):
    def test_full_candidate_requirement_coverage_is_executable(self):
        report = validate()
        self.assertEqual(CANDIDATE_SHA, report["candidate_commit"])
        self.assertEqual(len(REQUIRED_REQUIREMENTS), report["requirement_count"])
        self.assertEqual(REQUIRED_REQUIREMENTS, set(report["covered_requirements"]))
        self.assertEqual(len(REQUIRED_REQUIREMENTS), report["vector_count"])

    def test_unknown_critical_semantics_fail_closed(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "reject"},
            evaluate({"critical_supported": False}),
        )

    def test_current_revocation_is_not_projected_into_history(self):
        self.assertEqual(
            {"semantic_decision": "positive", "processing": "accept"},
            evaluate({"historical": True, "material_state": "revoked"}),
        )

    def test_stale_evidence_is_not_authoritative_negative(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "accept"},
            evaluate({"evidence_fresh": False}),
        )

    def test_transport_failure_is_not_semantic_negative(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "reject"},
            evaluate({"transport_ok": False}),
        )

    def test_v3_never_silently_downgrades(self):
        self.assertEqual(
            {"semantic_decision": "indeterminate", "processing": "reject"},
            evaluate({"negotiated_version": "v2", "legacy_fallback": True}),
        )


if __name__ == "__main__":
    unittest.main()
