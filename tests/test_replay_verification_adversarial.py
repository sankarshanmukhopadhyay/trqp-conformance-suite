"""Adversarial CTS-owned replay report consistency tests."""
import importlib.util
from pathlib import Path
import copy

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


def test_consistent_comparison_accepted():
    assert verifier.verify_v1(report()) == 0


def test_boolean_does_not_override_semantic_hash_mismatch():
    r = report()
    r["replay"]["semantic_sha256"] = "d"*64
    assert verifier.verify_v1(r) != 0


def test_target_state_mismatch_fails():
    r = report()
    r["replay"]["target_state"]["digest"] = "c"*64
    assert verifier.verify_v1(r) != 0


def test_missing_source_identity_fails():
    r = report()
    r["source"]["run_id"] = None
    assert verifier.verify_v1(r) != 0


def test_difference_count_mismatch_fails():
    r = report()
    r["summary"]["permitted_difference_count"] = 1
    assert verifier.verify_v1(r) != 0
