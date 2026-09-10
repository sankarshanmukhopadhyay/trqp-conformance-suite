---
owner: maintainers
last_reviewed: 2026-09-10
tier: 0
---

# TRQP Conformance Suite

The TRQP Conformance Suite is the **executable protocol-conformance authority** in the TRQP Operational Trust Stack. It maps TRQP requirements to repeatable tests, produces structured verdicts and replayable evidence, and exposes machine-readable outputs that downstream assurance tooling can consume without reinterpretation.

> **Current component release:** v1.10.0  
> **Current coordinated stack:** TRQP Stack 2026.2 — Ashoka  
> **Coordinated release candidate:** TRQP Stack 2026.3 — Banyan  
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
| Profile-consumable evidence schema | [`schemas/evidence/profile-consumable-conformance.schema.json`](schemas/evidence/profile-consumable-conformance.schema.json) |
| Portfolio integration | [`docs/portfolio-integration.md`](docs/portfolio-integration.md) |
| Documentation site | https://sankarshanmukhopadhyay.github.io/trqp-conformance-suite/ |

## Start here

For the validated multi-repository adoption path, start with the coordinated TRQP Stack release in the TRQP Assurance Hub. If you are implementing or evaluating CTS directly, use:

- [`docs/START_HERE.md`](docs/START_HERE.md) — role-based entry point;
- [`QUICKSTART.md`](QUICKSTART.md) — run the suite;
- [`docs/TRQP_Conformance_Philosophy.md`](docs/TRQP_Conformance_Philosophy.md) — conformance design principles;
- [`docs/evidence_bundles.md`](docs/evidence_bundles.md) — portable evidence model; and
- [`docs/portfolio-integration.md`](docs/portfolio-integration.md) — coordinated Stack relationship.

## v1.10.0 profile-aware evidence producer

v1.10.0 makes profile-consumable core-conformance evidence an explicit CTS producer contract. The exported artifact binds CTS results to the suite version, exact test-set revision, TRQP protocol version and binding, target/run identity, individual evidence references, and lifecycle/reassessment state.

Profile metadata is correlation context only. It cannot modify CTS core test semantics. Operational `ERROR`, `SKIP`, or unresolved states are exported as `INDETERMINATE`, never reinterpreted as negative authorization or recognition decisions. `NOT_APPLICABLE` remains distinct from failure.

The release retains the v1.9.x impact-aware reassessment capability: bounded reassessment is permitted only when material impact and affected tests are explicit; unknown impact fails toward a full rerun. CTS remains authoritative for conformance/replay reassessment consequences.

The candidate coordinated compatibility tuple is **CTS v1.10.0 / TSPP v0.17.0 / Assurance Hub v1.13.0**. Until Stack 2026.3 passes its coordinated release gate, **TRQP Stack 2026.2 — Ashoka remains the current coordinated Stack release**.

## Profile-aware evidence producer boundary

CTS may produce evidence that a named profile-aware consumer, such as the TRQP Assurance Hub, can correlate to a profile assessment. That does **not** make CTS a profile-policy authority.

The profile-consumable producer contract preserves:

- exact CTS suite version;
- test-set identity and content revision;
- TRQP protocol version and binding;
- target and run identity;
- individual CTS test results and evidence references; and
- current/reassessment/invalid lifecycle state.

Optional `profile_context` is correlation metadata only. It MUST NOT modify CTS core test semantics or convert an existing CTS result into a different conformance conclusion.

The responsibility boundary is:

| Observation | Authority |
|---|---|
| TRQP core/binding conformance and deterministic replay | CTS |
| Ecosystem-profile narrowing and extensions | Profile authority + Assurance Hub projection |
| Security/privacy posture and control semantics | TRQP-TSPP |
| DID/governance legitimacy and other external authority evidence | Applicable external authority/evidence source |
| Composition of independent evidence into a profile assurance conclusion | TRQP Assurance Hub |

The export helper is `scripts/build_profile_consumable_evidence.py`; its schema is `schemas/evidence/profile-consumable-conformance.schema.json`. Reassessment state is carried forward from the CTS lifecycle model so stale or materially affected core evidence cannot be presented as current merely because a consumer supplies matching profile metadata.

## Authority and scope

CTS is authoritative for executable TRQP conformance requirements, deterministic verdict and replay-evidence production, portable conformance evidence bundles, and replay/test interpretation implemented by the suite. CTS is **not** authoritative for the upstream TRQP protocol specification, TSPP security/privacy posture policy, Hub combined-assurance decisions, ecosystem-profile policy, or external certification.

## Conformance and replay model

A CTS requirement has a stable identifier, executable tests, explicit pass/fail criteria, required evidence, and profile-defined applicability. Deterministic replay asks whether conformance-semantic evidence is reproducible under the declared comparison policy; a failing conformance verdict may still be reproducible evidence, while undeclared semantic drift cannot pass.

## Evidence and auditability

Primary downstream artifacts include `artifacts/validation/cts-report.json`, replay determinism evidence, policy identity/version/hash provenance, requirement/negative-test traceability artifacts, and the profile-consumable conformance projection when requested. The machine-consumption boundary is declared in [`portfolio/stack-producer-contract.json`](portfolio/stack-producer-contract.json). Example or self-generated evidence is not independent certification.

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
