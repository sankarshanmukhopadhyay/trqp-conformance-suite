import unittest

from scripts.build_profile_consumable_evidence import build


BASE_REPORT = {
    "run_id": "run-1",
    "target_id": "registry-1",
    "generated_at": "2026-09-10T00:00:00Z",
    "results": [
        {"test_case_id": "TC-AUTHZ-001", "result": "PASS"},
        {"test_case_id": "TC-ERR-001", "result": "ERROR", "reason": "transport failure"},
    ],
}


def make(**kwargs):
    params = dict(
        report=BASE_REPORT,
        suite_version="1.8.0",
        protocol_version="2.0",
        binding="https-json",
        test_set_id="core-tests",
        test_set_revision_value="abc123",
        reassessment_state="CURRENT",
    )
    params.update(kwargs)
    return build(**params)


class ProfileConsumableEvidenceTests(unittest.TestCase):
    def test_preserves_exact_run_target_protocol_and_test_set(self):
        evidence = make()
        self.assertEqual(evidence["run"]["id"], "run-1")
        self.assertEqual(evidence["target"]["id"], "registry-1")
        self.assertEqual(evidence["protocol"], {"id": "trqp", "version": "2.0", "binding": "https-json"})
        self.assertEqual(evidence["test_set"]["revision"], "abc123")

    def test_operational_error_is_not_exported_as_negative_semantic_result(self):
        evidence = make()
        error = next(x for x in evidence["results"] if x["test_case_id"] == "TC-ERR-001")
        self.assertEqual(error["result"], "INDETERMINATE")

    def test_profile_context_is_correlation_metadata_only(self):
        baseline = make()
        profiled = make(profile_context={"id": "ayra-trqp", "version": "0.6.0-draft", "source_revision": "deadbeef"})
        self.assertEqual(baseline["results"], profiled["results"])
        self.assertEqual(profiled["profile_context"]["id"], "ayra-trqp")

    def test_same_core_evidence_can_be_correlated_to_multiple_profiles(self):
        a = make(profile_context={"id": "ayra-trqp"})
        b = make(profile_context={"id": "other-profile"})
        self.assertEqual(a["results"], b["results"])

    def test_reassessment_state_is_preserved(self):
        evidence = make(reassessment_state="REASSESS_REQUIRED")
        self.assertEqual(evidence["reassessment"]["state"], "REASSESS_REQUIRED")

    def test_unknown_cts_result_fails_closed(self):
        report = dict(BASE_REPORT)
        report["results"] = [{"test_case_id": "TC-X", "result": "MAYBE"}]
        with self.assertRaises(ValueError):
            make(report=report)


if __name__ == "__main__":
    unittest.main()
