---
layout: default
title: "Evidence Bundles"
nav_exclude: true
---

# Evidence Bundles

Evidence bundles are generated artifacts that make conformance results **auditable** and **replayable**.

## Design goals
- **Deterministic**: rerunning the same inputs against the same SUT should produce comparable outputs
- **Complete**: include enough request/response material to reproduce the decision
- **Safe**: do not leak secrets (API keys, private keys, access tokens)

## Recommended contents
- `bundle_descriptor.json`: machine-readable index of the bundle artifacts (kinds, paths, hashes)

- `run.json`: run metadata (run_id, timestamp, profile, SUT target)
- `verdicts.json`: per-test outcomes with reasons and assertions
- `requests/`: normalized requests used
- `responses/`: normalized responses captured
- `logs/`: runner logs (optional)

## Redaction policy
- Authorization headers and API keys MUST be redacted.
- Signed responses MAY be stored; private key material MUST NEVER be stored.

## Supply chain integrity artifacts (optional)

Evidence bundles MAY include supply chain integrity artifacts to support higher assurance evaluations:

- `software_sbom` (SBOM for the deployed artifact)
- `build_provenance` (build provenance / attestation)
- `openssf_scorecard_report` (OpenSSF Scorecard output or equivalent)

These are referenced by TSPP-SCI controls and surfaced in the Assurance Hub workflow.

## State-bound evidence scope

CTS v1.11.1 associates conformance and deterministic replay artifacts with a verified SHA-256 digest of the supplied target-state snapshot. Matching digests prove identical snapshot identity under the declared hashing contract; they do not attest that the snapshot corresponds to the current running deployment. An adopter must obtain appropriate build/deployment provenance, target ownership and post-change evidence where those claims affect reliance. The [Lotus coordinated release](https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub/releases/tag/trqp-stack-2026.4) validates cross-producer composition, not independent runtime certification.
