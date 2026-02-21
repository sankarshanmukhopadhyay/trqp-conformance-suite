# TRQP Conformance Suite

![CI](https://github.com/sankarshanmukhopadhyay/trqp-conformance-suite/actions/workflows/cts.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-Experimental-orange)

## Start here: TRQP Assurance Hub

Looking for the *single front door* across TRQP conformance + security/privacy assurance?

- Hub repo (onboarding, operating model, combined workflows): https://github.com/sankarshanmukhopadhyay/trqp-assurance-hub


Conformance Test Suite for the Trust Registry Query Protocol (TRQP).

This repository provides a profile-driven, evidence-oriented testing framework to validate TRQP implementations for interoperability, determinism, lifecycle correctness, and operational readiness.

This is an independent, open reference implementation. It is not an official artifact of the Trust over IP Foundation. The goal is to support ecosystem alignment and accelerate production-grade conformance discussions.

---

## Start Here

Choose the path that matches your role:

- **TRQP implementer**: run the **Baseline** profile, review `docs/START_HERE.md`, then compare results to the reference reports in `docs/reference-reports/`.
- **Spec author / working group participant**: review `docs/TRQP_Conformance_Philosophy.md` and `docs/ROADMAP.md` to see how requirements map to executable tests and evidence.
- **Ecosystem / governance / assurance**: read `docs/SOCIALIZING_NOTES.md` and `docs/evidence_bundle.schema.json` to understand the evidence contract and profile model.

---

## Why This Exists

Specifications describe behavior. Deployments require proof.

TRQP is designed as a lightweight verification rail across trust ecosystems. Without structured conformance testing, implementations may diverge in subtle but critical ways:

- Non-deterministic authorization outcomes
- Inconsistent lifecycle semantics
- Fragmented security posture
- Weak or undefined error modeling
- “Pass” results without verifiable evidence

This suite addresses those risks through executable, assertion-based testing.

---

## What You Get

- **Profiles** that scale assurance without changing core protocol semantics
  - Baseline, Enterprise, High-Assurance
- **Requirement IDs** mapped to executable tests
- **Deterministic verdict model** (PASS/FAIL/INCONCLUSIVE/NOT_APPLICABLE)
- **Evidence bundles** that are audit-friendly
  - transcripts, canonical payloads, hashes, manifest
  - signatures for High-Assurance runs (where configured)

---

## Core Principles

### Profile-Based Conformance

Different ecosystems require different assurance levels.

Profiles:

- **Baseline** — Minimal interoperable TRQP behavior
- **Enterprise** — Governance metadata and operational discipline
- **High-Assurance** — Deterministic state reference, replay resistance, stronger security enforcement

Profiles determine which requirements are mandatory.

---

### Assertion-Based Testing

Every normative requirement is mapped to:

- A stable requirement ID
- One or more executable tests
- Explicit pass/fail criteria
- Required evidence artifacts

A test does not pass without evidence.

---

### Deterministic Verdict Model

Each test produces one of:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`
- `NOT_APPLICABLE`

Verdicts are derived from requirement-level assertions, not HTTP status codes.

---

### Evidence-First Reporting

Each test run generates:

- Canonicalized request/response pairs
- Full HTTP transcripts
- Hashes of payloads
- A structured verdict manifest
- A signed evidence bundle (High-Assurance profile)

This enables auditability and reproducibility.

---

## Why Determinism Matters

TRQP decisions depend on registry state.

If identical inputs can produce different outputs under unclear state conditions, interoperability collapses.

High-Assurance profile requires:

- A declared `state_reference`
- Controlled fixture conditions
- Deterministic decision behavior for identical inputs

Without stable state reference, semantic conformance cannot be validated.

---

## Conformance Architecture Overview

```mermaid
graph TD
    A[Verifier / Client] --> B[TRQP Conformance Runner]
    B --> C[System Under Test]
    B --> D[Evidence Artifacts]
    D --> E[Manifest + Signature]
```

The runner executes profile-bound tests, captures transcripts, validates assertions, and produces a cryptographically verifiable evidence bundle.

---

## Repository Structure

```
profiles/         Conformance profiles
requirements/     Requirement catalog with stable IDs
tests/            Declarative test definitions
schemas/          JSON schemas for validation
cts/              Conformance test runner
examples/         Example TRQP-like service and configuration
docs/             Design philosophy and evidence model
```

---

## Running the Suite

### 1. Start the Example SUT

```
uvicorn examples.poc_service:app --reload
```

### 2. Run Baseline Profile

```
python cts/run.py   --profile profiles/baseline.yaml   --sut examples/sut.local.yaml   --out reports/run1
```

### 3. Run High-Assurance Profile

```
python cts/run.py   --profile profiles/high_assurance.yaml   --sut examples/sut.local.yaml   --out reports/runHA
```

---

## Evidence Artifacts

Each run produces:

```
reports/<run-id>/
  run.json
  verdicts.json
  manifest.json
  manifest.sig   (High-Assurance)
  cases/
  bundle.zip
```

The manifest includes cryptographic hashes of all artifacts.
High-Assurance profile signs the manifest for integrity verification.

See `docs/evidence_bundle.schema.json` for the evidence contract.

---

## Reference Reports

This repo includes sample evidence bundles under:

- `docs/reference-reports/sample_run_baseline/`
- `docs/reference-reports/sample_run_high_assurance/`

These are intended as concrete examples of what “good evidence” looks like, and how to verify manifests and signatures.

---

## Status

**Status:** Experimental

This repository is evolving and intended to inform structured conformance approaches for TRQP. It does not represent a formal certification authority.

---

## Roadmap

See `docs/ROADMAP.md`.

---

## Contributing

All additions must:

- Map to a requirement ID
- Produce structured evidence
- Respect profile definitions
- Avoid introducing undefined semantic assumptions

See `CONTRIBUTING.md` for guidelines.

---

## Strategic Positioning

This suite is intended to:

- Encourage interoperable TRQP implementations
- Support production-readiness discussions
- Provide a structured foundation for future conformance programs
- Reduce ambiguity in multi-ecosystem deployments

It does not assert normative authority over the TRQP specification.


## Repo hygiene and assurance artifacts

- Schema checks: `python scripts/schema_check.py`
- Preflight (optional): `python scripts/preflight.py --base-url https://your-sut/ --endpoint /.well-known/jwks.json`
- Traceability template: `docs/traceability.md`
- Evidence bundle guidance: `docs/evidence_bundles.md`


## AL3 / AL4 alignment

This repo includes convenience profiles `profiles/al3.yaml` and `profiles/al4.yaml` which reuse the high-assurance test set while annotating evidence bundles with an `assurance_level` field. Security posture semantics for AL3/AL4 are defined and audited in TRQP‑TSPP.
