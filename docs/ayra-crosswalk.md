---
owner: maintainers
last_reviewed: 2026-03-10
tier: 1
---

# Ayra Trust Network ↔ Conformance Suite Crosswalk

This document maps CTS/TSPP evidence artifacts to requirements for registries
operating within the Ayra Trust Network.

Reference: [Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html)

## Profile

Use the `ayra_baseline` profile for pre-certification testing:

```
python cts/run.py \
  --profile profiles/ayra_baseline.yaml \
  --sut examples/sut.local.yaml \
  --out reports/ayra-run
```

## Artifact mapping

| Ayra Requirement | CTS Artifact | TSPP Artifact | Notes |
|---|---|---|---|
| TRQP protocol conformance | `verdicts.json` (Baseline profile) | — | Must PASS TC-AUTHZ-001, TC-RECOG-001, TC-ERR-001 |
| Freshness semantics | `verdicts.json` (Enterprise: TRQP-FRESH-001/002) | `test_02_freshness.py` | Both harnesses must agree |
| Security posture (AL1) | — | TSPP AL1 harness output | metadata endpoint + rate limits + context allowlist |
| Signed responses (AL2) | `cases/auth_required.json` (High-Assurance) | `test_06_al2_signed_responses.py` | For Ayra high-consequence ecosystems |
| Governance publication | — | TSPP `/.well-known/trqp-metadata` (TSPP-META-01) | governance_framework_id in provenance |
| Evidence bundle integrity | `manifest.json` + `checksums.json` | `tspp_conformance_report.json` | Submit both bundles to Ayra conformance process |

## Assurance tier mapping

| Ayra Tier | CTS Profile | TSPP Level |
|---|---|---|
| Basic member registry | `ayra_baseline` | AL1 |
| Cross-ecosystem recognition registry | `ayra_baseline` + High-Assurance | AL2 |
| Sovereign / regulated ecosystem | `high_assurance` | AL3 (independent review) |

## Known gaps

The following Ayra-specific fields are not yet covered by automated tests.
Track in ROADMAP.md:

- `ecosystem_id` — Ayra network identifier for the registry's ecosystem
- `network_credential_type` — Ayra network credential type vocabulary
- Recognition chain depth validation (transitive recognition across Ayra clusters)
