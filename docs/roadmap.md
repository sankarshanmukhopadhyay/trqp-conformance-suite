---
layout: default
title: "Roadmap"
nav_exclude: true
---

# TRQP Conformance Suite Roadmap

**Last reviewed:** 2026-10-02

This roadmap records CTS-owned delivery priorities and its contribution to coordinated TRQP Stack releases. CTS retains authority over conformance execution, replay, and comparison semantics.

## Current coordinated baseline

TRQP Stack 2026.3 — Banyan remains the current coordinated baseline: CTS `v1.10.0`, TSPP `v0.17.0`, and Assurance Hub `v1.13.0`. CTS component development continues independently.

## October 2026 capability: state-bound conformance evidence

CTS v1.11.0 binds conformance and replay evidence to a verified SHA-256 target-state identity. This completes the prior state-snapshot maturity backlog by making the snapshot digest an explicit producer correlator rather than optional context.

The capability is coordinated with Assurance Hub issue #99 and TSPP state-bound posture work, but it is protocol-version neutral and does not depend on downstream candidate TRQP work. Publication of v1.11.0 does not itself advance the coordinated Stack release.

## September 2026 priority: bounded reassessment after change

**Coordinating issue:** https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/issues/39  
**CTS issue:** https://github.com/sankarshanmukhopadhyay/trqp-conformance-suite/issues/32  
**Target coordinated release:** TRQP Stack 2026.2 by 30 September 2026, subject to evidence readiness.

### CTS proposition

> A change that can affect TRQP conformance or replay semantics MUST trigger reassessment of affected evidence, while a proven non-material change may preserve reusable evidence. Unknown impact MUST fail toward broader reassessment.

### Required capability

Extend deterministic replay with conservative, machine-verifiable impact-aware reassessment. Candidate outputs are:

- `change-impact-report.json`;
- `reassessment-plan.json`;
- `reassessment-result.json`.

The contract should expose whether impact is known, affected and reusable tests where safely knowable, whether a full rerun is required, and a stable rationale code.

### Required pressure tests

- semantic protocol behavior changes;
- permitted volatile-field change;
- replay comparison-policy change;
- fixture change without semantic protocol drift;
- test-set/version change;
- unknown dependency change;
- unsupported partial rerun.

If CTS cannot establish a safe bounded impact set, a full rerun is required.

### Acceptance evidence

- machine-verifiable change-impact contract;
- bounded affected/reusable test evidence where safe;
- full-rerun behavior on unknown impact;
- deterministic replay regression coverage;
- negative tests rejecting unsupported partial reassessment;
- preserved replay-policy identity and provenance;
- synchronized producer contract and documentation.

## Candidate release decision

`v1.9.0` is a candidate only if bounded reassessment lands as a material capability. The Stack does not require a version bump for synchronization alone.

## Timing

| Target | Outcome |
|---|---|
| 6 Sep | change/impact contract aligned |
| 14 Sep | impact-aware reassessment capability ready |
| 20–25 Sep | participate in coordinated adversarial suite |
| 26 Sep | candidate tag/version decision frozen |
| 27–28 Sep | coordinated eligibility replay |

## Visible judgment

The implementation history must make visible when bounded reassessment is considered safe, when a full rerun is mandatory, which alternatives were rejected, and what evidence could falsify the bounded-impact claim.
