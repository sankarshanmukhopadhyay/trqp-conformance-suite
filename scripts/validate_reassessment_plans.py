#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "examples" / "lifecycle"


def load(name):
    with (FIXTURES / name).open(encoding="utf-8") as f:
        return json.load(f)


def validate(plan):
    assert plan.get("source_event_ref"), "source lifecycle event must be attributable"
    assert plan.get("source_authority") == "TRQP-TSPP", "upstream authority must remain explicit"
    assert plan.get("decision_authority") == "TRQP-CTS", "CTS owns reassessment planning"
    assert plan.get("policy_id"), "comparison/reassessment policy identity must be preserved"
    impact = plan.get("impact", {})
    for key in ["known", "affected_tests", "reusable_tests", "full_rerun_required", "rationale_code"]:
        assert key in impact, f"missing impact field: {key}"

    if plan["source_impact"] == "unknown":
        assert impact["full_rerun_required"] is True, "unknown impact must fail toward full rerun"
        assert impact["affected_tests"] == [] and impact["reusable_tests"] == [], "unknown impact cannot claim a bounded safe set"

    if plan["source_impact"] == "material" and impact["full_rerun_required"] is False:
        assert impact["affected_tests"], "bounded material reassessment requires explicit affected tests"

    if plan["source_impact"] == "non_material":
        assert impact["known"] is True, "reuse requires known non-material impact"
        assert impact["affected_tests"] == [], "non-material counter-case cannot claim affected tests"
        assert impact["reusable_tests"], "non-material reuse must identify reusable evidence"


def main():
    names = [
        "material-change.reassessment-plan.json",
        "unknown-impact.reassessment-plan.json",
        "non-material.reassessment-plan.json",
    ]
    for name in names:
        validate(load(name))

    probes = []
    unknown = load(names[1]); unknown["impact"]["full_rerun_required"] = False; probes.append(("unknown-bounded", unknown))
    material = load(names[0]); material["impact"]["affected_tests"] = []; probes.append(("material-no-scope", material))
    non_material = load(names[2]); non_material["impact"]["known"] = False; probes.append(("unknown-reuse", non_material))

    for label, probe in probes:
        try:
            validate(probe)
        except AssertionError:
            continue
        raise AssertionError(f"negative pressure test unexpectedly accepted: {label}")

    print("CTS reassessment plans satisfy fail-safe boundaries")


if __name__ == "__main__":
    main()
