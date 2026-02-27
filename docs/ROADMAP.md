# Roadmap

This roadmap is intentionally lightweight and focused on adoption and socialization.

## 2026 Q1: Socialization and trust signaling

- Done: onboarding docs (`START_HERE`, `SOCIALIZING_NOTES`, `FAQ`)
- Done: reference evidence bundles (`docs/reference-reports/`)
- Done: evidence bundle descriptor + checksums schemas (`schemas/evidence/`)
- Done: CI publishes evidence bundles as build artifacts (descriptor + checksums + bundle.zip)
- Done: Smoke profile for Hub combined-assurance workflow (`profiles/smoke.yaml`)
- Done: Hub crosswalk mapping (`docs/hub-crosswalk.md`)

## 2026 Q2: Deterministic replay and state models

- Planned: deterministic replay mode (`--replay <run-dir>`)
- Planned: state snapshot verification models (fixture ID, snapshot hash, signed snapshot)

## 2026 Q3: Security profiles and plugfests

- Planned: mTLS security profile
- Planned: interoperability plugfest mode and matrix generation

## 2026 Q4: Performance and operational readiness

- Planned: performance conformance harness and SLA-oriented checks


## Completed

- ✅ AL semantic lock to Assurance Hub (`al-contract.json` + explicit README/docs pointers)
