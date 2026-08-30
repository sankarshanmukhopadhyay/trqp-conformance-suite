---
owner: maintainers
last_reviewed: 2026-08-30
tier: 0
---

# TRQP Conformance Suite

The TRQP Conformance Suite is the **executable protocol-conformance authority** in the TRQP Operational Trust Stack. It maps TRQP requirements to repeatable tests, produces structured verdicts and replayable evidence, and exposes machine-readable outputs that downstream assurance tooling can consume without reinterpretation.

> **Current component release:** v1.9.1  
> **Current coordinated stack:** TRQP Stack 2026.1 — Coconut  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Primary role | Protocol conformance engine |
| Portfolio contract role | `conformance-test-authority` |
| Primary output | Conformance Report and portable evidence bundle |
| Validation | `make validate` |
| Assurance evidence | `make assurance-check` |
| Evidence output | `artifacts/validation/cts-report.json`, replay determinism and traceability evidence |
| Governance authority | [`GOVERNANCE.md`](GOVERNANCE.md) and [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) |
| Producer contract | [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json) |
| Portfolio integration | [`docs/portfolio-integration.md`](docs/portfolio-integration.md) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/trqp-conformance-suite/ |

## Start here

For the validated multi-repository adoption path, start with the coordinated TRQP Stack release in the TRQP Assurance Hub. If you are implementing or evaluating CTS directly, use:

- [`docs/START_HERE.md`](docs/START_HERE.md) — role-based entry point;
- [`QUICKSTART.md`](QUICKSTART.md) — run the suite;
- [`docs/TRQP_Conformance_Philosophy.md`](docs/TRQP_Conformance_Philosophy.md) — conformance design principles;
- [`docs/evidence_bundles.md`](docs/evidence_bundles.md) — portable evidence model; and
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — coordinated Stack relationship.

## v1.9.x reassessment capability

The v1.9 line adds impact-aware reassessment: bounded reassessment when material impact and affected tests are explicit, full rerun when impact is unknown, and attributable reuse for legitimate non-material change. v1.9.1 is a patch release that repairs the repository-status contract exposed by clean-room Stack execution; it does not change reassessment semantics.

CTS remains authoritative for conformance/replay reassessment consequences. It consumes TSPP materiality through the portable TIS lifecycle contract without redefining posture materiality or Hub assurance validity.

## Authority and scope

CTS is authoritative for executable TRQP conformance requirements, deterministic verdict and replay-evidence production, portable conformance evidence bundles, and replay/test interpretation implemented by the suite. CTS is **not** authoritative for the upstream TRQP protocol specification, TSPP security/privacy posture policy, Hub combined-assurance decisions, or external certification.

## Conformance and replay model

A CTS requirement has a stable identifier, executable tests, explicit pass/fail criteria, required evidence, and profile-defined applicability. Deterministic replay asks whether conformance-semantic evidence is reproducible under the declared comparison policy; a failing conformance verdict may still be reproducible evidence, while undeclared semantic drift cannot pass.

## Evidence and auditability

Primary downstream artifacts include `artifacts/validation/cts-report.json`, replay determinism evidence, policy identity/version/hash provenance, and requirement/negative-test traceability artifacts. The machine-consumption boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json). Example or self-generated evidence is not independent certification.

## Quick validation

```bash
make validate
make assurance-check
```

For local conformance and high-assurance execution, see [`QUICKSTART.md`](QUICKSTART.md).

## Governance and release policy

- [`GOVERNANCE.md`](GOVERNANCE.md) — repository-local authority and decision rights.
- [`docs/governance/release-policy.md`](docs/governance/release-policy.md) — component release policy.
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — relationship to coordinated Stack releases.

Component releases remain independently versioned. A new CTS release does not automatically cause a Stack release; the Hub publishes a coordinated release only after the complete tuple passes the Stack eligibility gate.

## License

Apache 2.0. See [`LICENSE`](LICENSE).
