"""Adversarial CTS-owned replay consistency tests using the repository's unittest runner."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("replay_verifier", ROOT / "scripts/verify_replay_determinism.py")
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def report():
    state = {"algorithm": "sha256", "digest": "a" * 64,
             "identity": "sha256:" + "a" * 64, "source": "snapshot.json", "status": "verified"}
    return {"report_version": "1.0.0", "policy": {"id": "p", "version": "1", "sha256": "c"*64},
            "source": {"run_id": "source", "semantic_sha256": "b"*64, "target_state": state},
            "replay": {"run_id": "replay", "semantic_sha256": "b"*64, "target_state": copy.deepcopy(state)},
            "summary": {"difference_count": 0, "permitted_difference_count": 0,
                        "prohibited_difference_count": 0},
            "differences": [], "deterministic": True}


class AdversarialReplayVerifierTests(unittest.TestCase):
    def test_consistent_comparison_accepted(self):
        self.assertEqual(verifier.verify_v1(report()), 0)

    def test_boolean_does_not_override_semantic_hash_mismatch(self):
        r = report()
        r["replay"]["semantic_sha256"] = "d"*64
        self.assertNotEqual(verifier.verify_v1(r), 0)

    def test_target_state_mismatch_fails(self):
        r = report()
        r["replay"]["target_state"]["digest"] = "c"*64
        self.assertNotEqual(verifier.verify_v1(r), 0)

    def test_missing_source_identity_fails(self):
        r = report()
        r["source"]["run_id"] = None
        self.assertNotEqual(verifier.verify_v1(r), 0)

    def test_difference_count_mismatch_fails(self):
        r = report()
        r["summary"]["permitted_difference_count"] = 1
        self.assertNotEqual(verifier.verify_v1(r), 0)
