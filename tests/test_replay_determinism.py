import json
import unittest
from pathlib import Path

from cts.determinism import classify_differences, diff_documents, semantic_sha256, summarize_differences

ROOT = Path(__file__).resolve().parent.parent
POLICY = json.loads((ROOT / "policies/replay-determinism.v1.json").read_text(encoding="utf-8"))


class ReplayDeterminismTests(unittest.TestCase):
    def test_equivalent_documents_are_deterministic(self):
        doc = {"run": {"profile_id": "baseline"}, "cases": {"TC-1": {"result": "PASS"}}}
        self.assertEqual(diff_documents(doc, doc), [])
        self.assertEqual(semantic_sha256(doc), semantic_sha256(doc))

    def test_permitted_volatile_difference_does_not_fail(self):
        original = {
            "run": {"test_run_id": "run-a", "profile_id": "baseline"},
            "cases": {"TC-1": {"elapsed_ms": 14, "result": "PASS"}},
        }
        replay = {
            "run": {"test_run_id": "run-b", "profile_id": "baseline"},
            "cases": {"TC-1": {"elapsed_ms": 0, "result": "PASS"}},
        }
        classified = classify_differences(diff_documents(original, replay), POLICY)
        summary = summarize_differences(classified)
        self.assertEqual(summary["prohibited_difference_count"], 0)
        self.assertEqual(summary["permitted_difference_count"], 2)

    def test_semantic_mutation_fails(self):
        original = {"cases": {"TC-1": {"response": {"status": 200}, "result": "PASS"}}}
        replay = {"cases": {"TC-1": {"response": {"status": 403}, "result": "FAIL"}}}
        classified = classify_differences(diff_documents(original, replay), POLICY)
        summary = summarize_differences(classified)
        self.assertGreater(summary["prohibited_difference_count"], 0)
        self.assertTrue(all(not d["permitted"] for d in classified))


if __name__ == "__main__":
    unittest.main()
