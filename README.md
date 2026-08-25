---
owner: maintainers
last_reviewed: 2026-08-25
tier: 0
---

# TRQP Conformance Suite

The TRQP Conformance Suite is the **executable protocol-conformance authority** in the TRQP Operational Trust Stack. It maps TRQP requirements to repeatable tests, produces structured verdicts and replayable evidence, and exposes machine-readable outputs that downstream assurance tooling can consume without reinterpretation.

> **Current component release:** v1.8.0  
> **Current coordinated stack:** TRQP Stack 2026.1 — Coconut  
> **Lifecycle:** Active  
> **Maturity:** Implementation draft  
> **Operational status:** Active validation

| Attribute | Value |
|---|---|
| Primary role | Protocol conformance engine |
| Portfolio contract role | `conformance-test-authority` |
| Primary output | Conformance Report and portable evidence bundle |
| Validation | `make validate` |
| Assurance evidence | `make assurance-check` |
| Producer contract | [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json) |
| Portfolio integration | [`docs/portfolio-integration.md`](docs/portfolio-integration.md) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/trqp-conformance-suite/ |

## Start here

If you want the **validated multi-repository adoption path**, start with **TRQP Stack 2026.1 — Coconut** in the TRQP Assurance Hub. That coordinated release tells you which CTS, TSPP, Hub, TSMM, and TIS versions have actually been exercised together.

If you are implementing or evaluating CTS directly, start with:

- [`docs/START_HERE.md`](docs/START_HERE.md) — role-based entry point;
- [`QUICKSTART.md`](QUICKSTART.md) — run the suite;
- [`docs/TRQP_Conformance_Philosophy.md`](docs/TRQP_Conformance_Philosophy.md) — conformance design principles;
- [`docs/evidence_bundles.md`](docs/evidence_bundles.md) — portable evidence model; and
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — coordinated Stack relationship.

## Coordinated Stack 2026.1 — Coconut

The current validated tuple is:

| Layer | Release | Authority / output |
|---|---:|---|
| TRQP-TSPP | v0.15.0 | Security/privacy controls and posture evidence |
| TRQP Conformance Suite | v1.8.0 | Protocol conformance and deterministic replay evidence |
| TRQP Assurance Hub | v1.11.0 | Combined assurance and coordinated release publication |
| TSMM | v0.24.0 | Semantic authority |
| TIS | v0.14.1 | Schema and portfolio authority |

For adopters, the coordinated release removes version-selection ambiguity. CTS v1.8.0 is the conformance/replay producer that was actually exercised in the declared tuple; the Hub consumes that evidence without redefining CTS semantics.

The coordinated release is a compatibility and assurance contract, not a fourth implementation product and not a transfer of authority between repositories.

## What v1.8.0 establishes

v1.8.0 makes deterministic replay a first-class machine-verifiable conformance invariant. It introduces a versioned replay comparison policy, separates conformance-semantic evidence from volatile execution metadata, emits replay determinism reports with policy/hash provenance, and fails closed on undeclared semantic drift.

See [`RELEASE_NOTES_v1.8.0.md`](RELEASE_NOTES_v1.8.0.md).

## Authority and scope

CTS is authoritative for:

- executable TRQP conformance requirements;
- deterministic verdict and replay-evidence production;
- portable conformance evidence bundles; and
- the replay/test interpretation implemented by this suite.

CTS is **not** authoritative for the upstream TRQP protocol specification, TSPP security/privacy posture policy, Hub combined-assurance decisions, or external certification. The coordinated Stack release preserves those boundaries.

## Conformance and replay model

A CTS requirement should have a stable requirement identifier, executable tests, explicit pass/fail criteria, required evidence, and profile-defined applicability. Verdicts are assertion-derived and may be `PASS`, `FAIL`, `INCONCLUSIVE`, or `NOT_APPLICABLE`.

Deterministic replay asks a different question from conformance: whether the conformance-semantic evidence is reproducible under the declared comparison policy. A failing conformance verdict can still be reproducible evidence; undeclared semantic drift cannot.

## Evidence and auditability

A CTS run produces a self-describing evidence bundle. Primary downstream artifacts include:

- `artifacts/validation/cts-report.json`;
- replay determinism evidence;
- policy identity/version/hash provenance; and
- requirement/negative-test traceability artifacts.

The current machine-consumption boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json). Example or self-generated evidence is not independent assurance or certification.

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

Component releases remain independently versioned. A new CTS release does not automatically cause a new Stack release; the Hub cuts a new coordinated release only after the complete tuple passes the Stack eligibility gate.

## License

Apache 2.0. See [`LICENSE`](LICENSE).
