# TRQP Conformance Suite v1.9.0 — Impact-aware Reassessment

This release adds executable reassessment planning for TRQP Stack 2026.2 lifecycle change evidence.

## Added

- bounded reassessment plans for known material change with explicit affected tests;
- full rerun on unknown impact;
- non-material reuse counter-case with explicit reusable tests;
- negative validation preventing unsupported partial reassessment and missing source lineage.

## Authority boundary

CTS owns conformance/replay reassessment consequence. It consumes TSPP materiality evidence through the portable TIS lifecycle contract without redefining posture materiality or Hub assurance validity.

## Stack relationship

v1.9.0 is the CTS component candidate for TRQP Stack 2026.2. Coordinated release eligibility remains Hub-owned and requires the exact immutable tuple to pass clean bootstrap, replay, lifecycle, and human judgment gates.
