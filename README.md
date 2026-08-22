---
owner: maintainers
last_reviewed: 2026-08-22
tier: 0
---

# TRQP Conformance Suite

The TRQP Conformance Suite is the **executable protocol-conformance authority** in the TRQP Operational Trust Stack. It maps TRQP requirements to repeatable tests, produces structured verdicts and replayable evidence, and exposes machine-readable outputs that downstream assurance tooling can consume without reinterpretation.

> **Current release:** v1.8.0  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation  
> **Specification status:** Candidate specification

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Primary role | Protocol conformance engine |
| Portfolio contract role | `conformance-test-authority` |
| Primary output | Conformance Report and portable evidence bundle |
| Validation | `make validate` |
| Assurance evidence | `make assurance-check` |
| Evidence output | `artifacts/validation/cts-report.json`, `artifacts/traceability/cts-requirement-coverage.json`, `artifacts/traceability/negative-test-coverage.json` |
| Governance authority | [`GOVERNANCE.md`](GOVERNANCE.md) and [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) |
| Portfolio integration | [`portfolio/integration-contract.json`](portfolio/integration-contract.json) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/trqp-conformance-suite/ |

![CI](https://github.com/sankarshanmukhopadhyay/trqp-conformance-suite/actions/workflows/cts.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-Active%20Validation-brightgreen)

## What v1.8.0 establishes

v1.8.0 makes deterministic replay a first-class, machine-verifiable conformance invariant.

- Retains **Trust Systems Meta-Model (TSMM) v0.24.0** as semantic authority for the TRQP binding.
- Retains **Trust Infrastructure Schemas (TIS) v0.14.1** as schema and portfolio-authority baseline.
- Introduces the versioned `trqp-replay-determinism` comparison policy.
- Canonicalizes conformance-semantic evidence separately from volatile execution metadata.
- Emits schema-valid replay determinism reports with policy identity/version/hash provenance and JSON Pointer-level differences.
- Fails closed on semantic drift while allowing explicitly declared execution volatility.
- Attaches replay determinism evidence to the fixture-pinned Baseline evidence bundle for downstream Assurance Hub consumption.
- Keeps live Baseline execution as an interoperability check rather than treating live transport timing and metadata as deterministic evidence.

See [`RELEASE_NOTES_v1.8.0.md`](RELEASE_NOTES_v1.8.0.md) for the release record.

## Authority and scope

CTS has repository-local authority over:

- executable TRQP conformance requirements;
- deterministic verdict and replay-evidence production;
- portable conformance evidence bundles; and
- the test/evidence interpretation implemented by this suite.

CTS **does not** own the TRQP protocol specification, TSPP security-posture policy, final ecosystem assurance decisions, or external certification. Those boundaries are declared in [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) and [`portfolio/integration-contract.json`](portfolio/integration-contract.json).

## Where this fits

| Layer | Repository role | Primary output |
|---|---|---|
| TRQP-TSPP v0.15.0 | Security/privacy posture computation | Posture Report and control evidence |
| TRQP Conformance Suite v1.8.0 | Executable protocol conformance | Conformance Report, determinism report and evidence bundle |
| TRQP Assurance Hub v1.10.0 | Evidence aggregation and assurance publication | Combined Assurance Manifest and assurance decision |

Shared authorities:

| Authority | Version | Purpose |
|---|---:|---|
| Trust Systems Meta-Model | 0.24.0 | TRQP semantic binding and semantic concepts |
| Trust Infrastructure Schemas | 0.14.1 | Portfolio relationships, repository authority and validation-result contracts |

The CTS portfolio integration is invalid when required evidence is missing, the normative TSPP source is incompatible, the replay comparison policy is incompatible, or the declared semantic/schema authority versions no longer match.

## Conformance model

Every executable requirement is intended to provide:

- a stable requirement identifier;
- one or more executable tests;
- explicit pass/fail criteria;
- required evidence artifacts; and
- a profile-defined applicability/assurance context.

Verdicts are assertion-derived rather than inferred from HTTP status alone:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`
- `NOT_APPLICABLE`

A failing verdict is valid conformance evidence. Deterministic replay asks whether conformance-semantic evidence is equivalent under the declared comparison policy, not whether every verdict is PASS.

## Profiles

The suite supports multiple assurance postures without changing core TRQP semantics:

- **Smoke** — fast deterministic sanity check.
- **Baseline** — minimum interoperable TRQP behavior.
- **Enterprise** — governance metadata and stronger operational discipline.
- **High-Assurance** — deterministic state reference, stronger security controls, evidence integrity and replay expectations.
- **Ayra Baseline** — Ayra-specific pre-certification profile.
- **DeDi Experimental** — schema-oriented experimental support for decentralized-directory artifacts.

Profiles determine which requirements are mandatory and what evidence must be emitted.

## Evidence bundle

A CTS run produces a self-describing bundle under `reports/<run-id>/`. Treat `bundle_descriptor.json` as the index of record.

| Artifact | Purpose |
|---|---|
| `run.json` | Run metadata, profile, SUT, timing and tool version |
| `verdicts.json` | Per-test semantic verdicts |
| `manifest.json` | Integrity manifest |
| `checksums.json` | SHA-256 checksums for key artifacts |
| `manifest.sig` | High-assurance signature when signing is configured |
| `cases/*.json` | Replayable case evidence/transcripts |
| `determinism-report.json` | Policy-aware deterministic replay verdict and JSON Pointer differences |
| `replay-determinism-policy.json` | Versioned comparison policy captured with deterministic evidence |
| `bundle_descriptor.json` | Machine-readable evidence index |
| `cts-report.json` | Hub-ready conformance report |
| `bundle.zip` | Optional portable package |

## Start here

- [`docs/START_HERE.md`](docs/START_HERE.md) — role-based entry point.
- [`QUICKSTART.md`](QUICKSTART.md) — run the suite.
- [`docs/TRQP_Conformance_Philosophy.md`](docs/TRQP_Conformance_Philosophy.md) — conformance design principles.
- [`docs/evidence_bundles.md`](docs/evidence_bundles.md) — evidence bundle model.
- [`docs/reference-reports/`](docs/reference-reports/) — reference output examples.
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — synchronized TRQP portfolio integration.
- [`docs/tis-evidence-contract.md`](docs/tis-evidence-contract.md) — TIS evidence projection.
- [`docs/governance/release-policy.md`](docs/governance/release-policy.md) — release governance.
- [`docs/governance/change-intake.md`](docs/governance/change-intake.md) — change intake criteria.

## Quick validation

Run the repository governance/schema gate:

```bash
make validate
```

Run the cross-stack negative-case assurance checks:

```bash
make assurance-check
```

A typical local conformance run is:

```bash
uvicorn examples.poc_service:app --reload
python cts/run.py \
  --profile profiles/baseline.yaml \
  --sut examples/sut.local.yaml \
  --out reports/run1
```

For high-assurance evaluation:

```bash
python cts/run.py \
  --profile profiles/high_assurance.yaml \
  --sut examples/sut.local.yaml \
  --out reports/runHA
```

Copy `examples/sut.local.yaml.example` to `examples/sut.local.yaml` and generate fresh local signing material before running profiles that require it.

## Determinism and replay

Deterministic evidence is a first-class conformance property. CTS distinguishes:

1. **whether the SUT conforms**, and
2. **whether the conformance-semantic evidence can be reproduced**.

The normative CI determinism gate uses the fixture-pinned Baseline run, where inputs, responses, timestamp and run identity are controlled. The replay comparison policy explicitly classifies volatile paths such as run identifiers, output labels and elapsed timings. All other differences are prohibited by default.

`determinism-report.json` records every differing JSON Pointer, whether it is permitted, the policy identity/version/hash, and semantic SHA-256 digests. A source FAIL reproduced without semantic change remains deterministic evidence; a controlled semantic mutation fails the determinism gate.

## Repository map

| Path | Purpose |
|---|---|
| `requirements/` | Stable conformance requirement catalogue |
| `profiles/` | Conformance profiles |
| `tests/` | Declarative and determinism test definitions |
| `cts/` | Conformance runner and replay/determinism logic |
| `policies/` | Versioned executable comparison/governance policies |
| `schemas/` | Report, evidence and ecosystem schemas |
| `examples/` | Example SUT/configuration and fixtures |
| `artifacts/validation/` | Generated validation evidence |
| `artifacts/traceability/` | Requirement and negative-test coverage evidence |
| `portfolio/` | Cross-repository integration contract |
| `docs/` | Conformance philosophy, evidence model, mappings and adoption guidance |

## Additional interoperability support

- [`docs/directory-artifact-validation.md`](docs/directory-artifact-validation.md) — authoritative directory artifact validation.
- [`docs/UNTP_DIA_SUPPORT.md`](docs/UNTP_DIA_SUPPORT.md) — UNTP Digital Identity Anchor support.
- [`docs/ayra-crosswalk.md`](docs/ayra-crosswalk.md) — Ayra pre-certification crosswalk.
- [`docs/certification-alignment.md`](docs/certification-alignment.md) — Candidate Trust Registry Assurance & Certification Baseline alignment.
- [`docs/reference/dedi-mapping-matrix.md`](docs/reference/dedi-mapping-matrix.md) — experimental DeDi mapping.

## Evidence and auditability

CTS evidence retains the producer version, execution context, requirement/test identity, verdict, checksums, captured case material, determinism decision and comparison-policy provenance needed for downstream review. Example or self-generated evidence does not constitute independent assurance or certification.

## Documentation site

GitHub Pages uses Just the Docs and is deployed from `main` through GitHub Actions. Repository administrators should configure **Settings → Pages → Source: GitHub Actions**.

Documentation governance: [`docs/governance/README.md`](docs/governance/README.md).

## Contributing

Changes to executable conformance behavior should map to stable requirement IDs, produce structured evidence, respect profile semantics, and avoid introducing undefined protocol assumptions. Changes to replay determinism policy alter the assurance claim and therefore require explicit review and versioned policy provenance. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Apache 2.0. See [`LICENSE`](LICENSE).
