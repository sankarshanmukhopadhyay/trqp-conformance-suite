# Roadmap

This roadmap is intentionally lightweight and focused on adoption and socialization.

## 2026 Q1: Socialization and trust signaling

- Done: Operational Trust Stack Maturity Release governance (`docs/governance/release-policy.md`, `docs/governance/change-intake.md`, `docs/release-validation.md`)
- Done: onboarding docs (`START_HERE`, `SOCIALIZING_NOTES`, `FAQ`)
- Done: reference evidence bundles (`docs/reference-reports/`)
- Done: evidence bundle descriptor + checksums schemas (`schemas/evidence/`)
- Done: CI publishes evidence bundles as build artifacts (descriptor + checksums + bundle.zip)
- Done: Smoke profile for Hub combined-assurance workflow (`profiles/smoke.yaml`)
- Done: Hub crosswalk mapping (`docs/hub-crosswalk.md`)
- Done: `--dry-run` and `--list-tests` CLI flags for developer tooling
- Done: `identifiers:` SUT config block for real-SUT parameterization
- Done: JSONPath wildcard token indexing fix
- Done: `QUICKSTART.md` for fast onboarding

## 2026 Q2: Deterministic replay and state models

- ✅ Deterministic replay mode (`--replay <run-dir>`): re-evaluates assertion logic over captured case files, emits `replay-report.json` with verdict diffs.
- ✅ Fixture-pinned run mode (`--fixture-set <file>`): canned responses with SHA-256 provenance embedded in `run.json`.
- ✅ `--generated-at` timestamp pinning: all evidence artifact timestamps are now deterministic when a value is supplied.
- Maturity backlog: state snapshot verification (fetch, hash, and gate on declared `state_snapshot_url`)

## 2026 Q3: Security profiles and plugfests

- Maturity backlog: mTLS security profile when adopter demand justifies the additional operational burden
- Done: scenario interop matrix generation is available through `scripts/generate_interop_matrix.py`; future plugfest work should build on that artifact instead of introducing a new report shape.

## 2026 Q4: Performance and operational readiness

- Maturity backlog: performance conformance harness and SLA-oriented checks.


## Completed

- ✅ AL semantic lock to Assurance Hub (`al-contract.json` + explicit README/docs pointers)
- ✅ Runner refactored into named functions for testability
- ✅ TIS evidence contract and optional evidence descriptor projection metadata for Hub v1.8.0 runtime assurance.


## Release readiness and adoption focus

- `--dry-run` and `--list-tests` flags enable safer CI integration and developer inspection.
- Identifier parameterization via `sut.yaml` allows real SUTs to run the suite without modifying core tests.
- JSONPath wildcard bug fixed for correct assertion evaluation on array paths.
- QUICKSTART and expanded SECURITY documentation complete.
- TIS projection metadata allows CTS evidence to be consumed by downstream assurance workflows without changing core protocol test semantics.
- Future releases follow the maturity release policy: small wording, link, and metadata edits are batched unless they correct a security, CI, schema, or adoption blocker.

_Last updated: 2026-07-03_

## UNTP DIA considerations

Where a directory uses UNTP Digital Identity Anchor (DIA) / Identity Resolver (IDR), conformance evidence SHOULD include DIA context references and resolver documentation. The CTS validator includes lightweight checks for DIA context wiring when `identity_anchor.anchor_type` indicates UNTP DIA.
