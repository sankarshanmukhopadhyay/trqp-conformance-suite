---
owner: maintainers
last_reviewed: 2026-03-10
tier: 1
---

# Ayra Trust Network ↔ Conformance Suite Crosswalk

This document maps CTS and TSPP evidence artifacts to requirements for registries
operating within the Ayra Trust Network.

Reference: [Ayra TRQP Profile v0.5.0-draft](https://ayraforum.github.io/ayra-trust-registry-resources/) |
[Ayra Implementers Guide](https://ayraforum.github.io/ayra-trust-registry-resources/guides/) |
[Ayra TRQP Profile API](https://ayraforum.github.io/ayra-trust-registry-resources/api.html)

---

## Running the Ayra baseline profile

Use the `ayra_baseline` profile for pre-certification testing:

```bash
python cts/run.py \
  --profile profiles/ayra_baseline.yaml \
  --sut examples/sut.local.yaml \
  --out reports/ayra-run
```

This profile extends `enterprise` and additionally gates on:

- `TRQP-FRESH-001/002` — freshness fields on both authorization and recognition responses
- `TRQP-RECOG-001/002` — recognition endpoint correctness
- `TRQP-SEC-001` — security baseline
- `TRQP-ERR-RFC7807` — RFC 7807 Problem Details on all error responses (Ayra MUST)
- `TC-AYRA-META-001` through `TC-AYRA-LKP-003` — Ayra extension endpoint smoke tests

### Schema note

The `ayra_baseline` profile overrides the default `authz_response` and `recog_response`
schemas with `schemas/ayra/authz_response.schema.json` and `schemas/ayra/recog_response.schema.json`.
These match the flat response shape in the Ayra Implementers Guide, which differs from
the wrapped `decision` object in the core CTS schema. Ensure your registry returns the
Ayra flat shape or the profile validation will fail.

---

## Artifact mapping

| Ayra Requirement | CTS Artifact | TSPP Artifact | Notes |
|---|---|---|---|
| TRQP protocol conformance | `verdicts.json` (Baseline profile) | — | Must PASS TC-AUTHZ-001, TC-RECOG-001, TC-ERR-001 |
| Freshness semantics | `verdicts.json` (Enterprise: TRQP-FRESH-001/002) | `test_02_freshness.py` | Both harnesses must agree |
| RFC 7807 error format | `verdicts.json` (TRQP-ERR-RFC7807) | `test_04_uniform_errors.py` | Ayra MUST |
| Security posture (AL1) | — | TSPP AL1 harness output | metadata + rate limits + context allowlist |
| JWS-signed responses (MUST for all Ayra tiers) | `cases/auth_required.json` (High-Assurance) | `test_06_al2_signed_responses.py` | Required at Basic tier, not optional |
| Governance publication | — | TSPP `/.well-known/trqp-metadata` (TSPP-META-01) | `governance_framework_id` in provenance |
| Evidence bundle integrity | `manifest.json` + `checksums.json` | `tspp_conformance_report.json` | Submit both bundles to Ayra |
| Ayra extension endpoints | `verdicts.json` (TC-AYRA-*) | — | `/metadata`, `/entities/*`, `/ecosystems/*`, `/lookups/*` |
| Recognition security | — | `test_10_recognition_security.py` | NEW: POST /recognition security controls |

---

## Assurance tier mapping

| Ayra Tier | CTS Profile | TSPP Level |
|---|---|---|
| Basic member registry | `ayra_baseline` | AL1 + AL2 (JWS MUST) |
| Cross-ecosystem recognition registry | `ayra_baseline` + High-Assurance | AL2 |
| Sovereign / regulated ecosystem | `high_assurance` | AL3 (independent review) |

---

## Ayra identifier requirements

The Ayra Profile mandates `did:webvh` for all ecosystem, trust registry, and cluster
identifiers. This is not yet validated by CTS automated tests. The following manual
checks are required before Ayra submission:

1. Ecosystem DID is `did:webvh` with ≥ 2 service endpoints:
   - EGF endpoint at service profile `https://ayra.forum/profiles/trqp/egfURI/v1`
   - Trust Registry endpoint at `https://ayra.forum/profiles/trqp/tr/v2` (type: `TrustRegistryService`)
2. Trust Registry DID is `did:webvh` with ≥ 1 service endpoint at `https://ayra.forum/profiles/trqp/tr/v2`
3. Cluster DIDs (if applicable) are `did:webvh` with ≥ 1 trust metaregistry endpoint

Automated `did:webvh` format validation is tracked as a future enhancement.

---

## Two-step verifier flow

The Ayra Implementers Guide describes the canonical verification pattern for relying
parties. CTS tests both steps:

**Step 1 — Check ecosystem recognition:**

```json
POST /recognition
{
  "entity_id": "{target_ecosystem_did}",
  "authority_id": "did:webvh:ayra.forum",
  "action": "recognize",
  "resource": "ecosystem"
}
```

**Step 2 — Check entity authorization:**

```json
POST /authorization
{
  "entity_id": "{entity_did}",
  "authority_id": "{target_ecosystem_did}",
  "action": "issue",
  "resource": "credential:driverlicense"
}
```

TC-AYRA-ECO-001 and TRQP-RECOG-001/002 gate on Step 1 correctness. TC-AUTHZ-001 gates
on Step 2. Both must PASS for a complete Ayra conformance picture.

---

## Known gaps

The following Ayra-specific requirements are not yet covered by automated tests.

| Gap | Tracking |
|---|---|
| `did:webvh` format validation on request/response fields | Future CTS enhancement |
| EGF service endpoint resolution from ecosystem DID document | Future CTS enhancement |
| Recognition chain depth (transitive recognition across clusters) | CTS ROADMAP |
| Ayra network registration (governance review, DID submission) | Out of scope for toolset |
