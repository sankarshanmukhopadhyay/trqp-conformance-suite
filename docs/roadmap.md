---
layout: default
title: "Roadmap"
nav_exclude: true
owner: maintainers
last_reviewed: 2026-08-28
---

# TRQP Conformance Suite Roadmap

This roadmap records the Conformance Suite contribution to the coordinated **TRQP Stack 2026.2** planning target for 30 September 2026. Coordinated release authority remains with the TRQP Assurance Hub. CTS retains authority over executable conformance requirements, verdicts, evidence bundles, and replay-comparison semantics.

## Current baseline

CTS v1.8.0 participates in TRQP Stack 2026.1 — Coconut and makes deterministic replay a first-class machine-verifiable conformance invariant.

## September governing question

> After a change, can CTS determine which conformance evidence must be regenerated and which evidence may safely remain reusable, without allowing unknown impact to justify an incomplete reassessment?

The target is **impact-aware bounded reassessment**, not an assumption that every change can be incrementally tested.

## Target capability

Candidate evidence flow:

```text
previous CTS evidence
        +
change evidence
        +
comparison/test policy
        ↓
change impact analysis
        ↓
affected tests + reusable tests + full-rerun requirement
        ↓
reassessment plan
        ↓
reassessment result
```

Candidate artifacts include:

- `change-impact-report.json`;
- `reassessment-plan.json`; and
- `reassessment-result.json`.

Artifact names may change during implementation; the required semantics must remain machine-verifiable.

## Required work

### 1. Define impact evidence

The impact result should identify whether impact is known, which tests/evidence are affected, which prior results remain reusable where provable, whether a full rerun is required, and a stable rationale/policy identity.

### 2. Bound partial reassessment

Partial reruns are allowed only when the impact evidence positively justifies their scope. A claimed partial rerun without sufficient impact evidence must be rejected.

### 3. Fail safely on unknown impact

**Invariant:** unknown or unbounded impact requires broader/full reassessment. Missing impact evidence must never be interpreted as evidence that no tests are affected.

### 4. Preserve deterministic replay

The v1.8.0 replay contract remains a prerequisite. Impact-aware reassessment must not weaken replay determinism, comparison-policy provenance, semantic-drift detection, or portable evidence integrity.

## Pressure tests

At minimum:

| Change | Expected CTS disposition |
|---|---|
| protocol-semantic behavior changes | affected tests rerun / full rerun as required |
| only policy-declared volatile output changes | semantic evidence may remain reusable |
| replay comparison policy changes | replay/reassessment required |
| fixture changes with known bounded impact | bounded rerun only with evidence |
| test-set version changes | impact explicitly evaluated |
| dependency impact cannot be established | full/broader rerun |
| partial rerun claimed without impact evidence | reject |

Tests must demonstrate the boundaries between legitimate reuse and unsafe false continuity.

## Candidate release

`v1.9.0` is a planning hypothesis. It should be released only if CTS gains material impact/reassessment capability with machine-readable evidence, negative cases, documentation, and preserved deterministic replay. Otherwise the current CTS release remains authoritative and the Stack candidate must adapt.

## Target dates

- **1–6 Sep:** agree common change/invalidation boundary with Hub/TSPP/TIS.
- **7–14 Sep:** implement impact-aware reassessment and evidence.
- **by 20 Sep:** resolve policy/authority/schema compatibility implications.
- **20–25 Sep:** execute coordinated adversarial cases.
- **26 Sep:** candidate freeze if eligible.

## Release acceptance evidence

CTS is ready for the coordinated candidate only when:

- affected/reusable scope is machine-reviewable;
- unknown impact fails toward broader reassessment;
- partial reassessment without sufficient impact evidence is rejected;
- deterministic replay remains intact;
- material and legitimate non-material pressure cases are executable;
- producer evidence retains run, target, policy, version, and integrity provenance; and
- existing conformance behavior has no unexplained regression.

## Visible judgment

The implementation issue/PR should record the proposition, assumptions used to define bounded impact, alternatives genuinely considered, cases that could falsify safe partial reassessment, rejected approaches where applicable, and residual uncertainty. The release decision must explain why bounded reassessment is safe for the cases CTS claims to support.
