# TRQP Conformance Suite

![CI](https://github.com/sankarshanmukhopadhyay/trqp-conformance-suite/actions/workflows/cts.yml/badge.svg)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-Experimental-orange)

Conformance Test Suite for the Trust Registry Query Protocol (TRQP).

This repository provides a profile-driven, evidence-oriented testing
framework to validate TRQP implementations for interoperability,
determinism, lifecycle correctness, and operational readiness.

This is an independent, open reference implementation. It is not an
official artifact of the Trust over IP Foundation. The goal is to
support ecosystem alignment and accelerate production-grade conformance
discussions.

------------------------------------------------------------------------

## Why This Exists

Specifications describe behavior. Deployments require proof.

TRQP is designed as a lightweight verification rail across trust
ecosystems. Without structured conformance testing, implementations may
diverge in subtle but critical ways:

-   Non-deterministic authorization outcomes\
-   Inconsistent lifecycle semantics\
-   Fragmented security posture\
-   Weak or undefined error modeling\
-   "Pass" results without verifiable evidence

This suite addresses those risks through executable, assertion-based
testing.

------------------------------------------------------------------------

## Core Principles

### Profile-Based Conformance

Different ecosystems require different assurance levels.

Profiles:

-   **Baseline** --- Minimal interoperable TRQP behavior\
-   **Enterprise** --- Governance metadata and operational discipline\
-   **High-Assurance** --- Deterministic state reference, replay
    resistance, stronger security enforcement

Profiles determine which requirements are mandatory.

------------------------------------------------------------------------

### Assertion-Based Testing

Every normative requirement is mapped to:

-   A stable requirement ID\
-   One or more executable tests\
-   Explicit pass/fail criteria\
-   Required evidence artifacts

A test does not pass without evidence.

------------------------------------------------------------------------

### Deterministic Verdict Model

Each test produces one of:

-   `PASS`\
-   `FAIL`\
-   `INCONCLUSIVE`\
-   `NOT_APPLICABLE`

Verdicts are derived from requirement-level assertions, not HTTP status
codes.

------------------------------------------------------------------------

### Evidence-First Reporting

Each test run generates:

-   Canonicalized request/response pairs\
-   Full HTTP transcripts\
-   Hashes of payloads\
-   A structured verdict manifest\
-   A signed evidence bundle (High-Assurance profile)

This enables auditability and reproducibility.

------------------------------------------------------------------------

## Why Determinism Matters

TRQP decisions depend on registry state.

If identical inputs can produce different outputs under unclear state
conditions, interoperability collapses.

High-Assurance profile requires:

-   A declared `state_reference`\
-   Controlled fixture conditions\
-   Deterministic decision behavior for identical inputs

Without stable state reference, semantic conformance cannot be
validated.

------------------------------------------------------------------------

## Conformance Architecture Overview

``` mermaid
graph TD
    A[Verifier / Client] --> B[TRQP Conformance Runner]
    B --> C[System Under Test]
    B --> D[Evidence Artifacts]
    D --> E[Manifest + Signature]
```

The runner executes profile-bound tests, captures transcripts, validates
assertions, and produces a cryptographically verifiable evidence bundle.

------------------------------------------------------------------------

## Repository Structure

    profiles/         Conformance profiles
    requirements/     Requirement catalog with stable IDs
    tests/            Declarative test definitions
    schemas/          JSON schemas for validation
    cts/              Conformance test runner
    examples/         Example TRQP-like service and configuration
    docs/             Design philosophy and evidence model

------------------------------------------------------------------------

## Running the Suite

### 1. Start the Example SUT

    uvicorn examples.poc_service:app --reload

### 2. Run Baseline Profile

    python cts/run.py   --profile profiles/baseline.yaml   --sut examples/sut.local.yaml   --out reports/run1

### 3. Run High-Assurance Profile

    python cts/run.py   --profile profiles/high_assurance.yaml   --sut examples/sut.local.yaml   --out reports/runHA

------------------------------------------------------------------------

## Evidence Artifacts

Each run produces:

    reports/<run-id>/
      run.json
      verdicts.json
      manifest.json
      manifest.sig   (High-Assurance)
      cases/
      bundle.zip

The manifest includes cryptographic hashes of all artifacts.\
High-Assurance profile signs the manifest for integrity verification.

------------------------------------------------------------------------

## Sample Signed Conformance Report

A reference signed evidence bundle will be added under:

    docs/reference-reports/

This will demonstrate:

-   Deterministic replay\
-   Manifest hashing\
-   Signature verification workflow

------------------------------------------------------------------------

## Status

**Status:** Experimental

This repository is evolving and intended to inform structured
conformance approaches for TRQP. It does not represent a formal
certification authority.

------------------------------------------------------------------------

## Roadmap

Planned enhancements:

-   Formal evidence bundle schema\
-   State snapshot verification model\
-   mTLS security profile\
-   Performance and SLA validation\
-   Reference conformance reports\
-   CI reproducibility improvements

------------------------------------------------------------------------

## Contributing

All additions must:

-   Map to a requirement ID\
-   Produce structured evidence\
-   Respect profile definitions\
-   Avoid introducing undefined semantic assumptions

See `CONTRIBUTING.md` for guidelines.

------------------------------------------------------------------------

## Strategic Positioning

This suite is intended to:

-   Encourage interoperable TRQP implementations\
-   Support production-readiness discussions\
-   Provide a structured foundation for future conformance programs\
-   Reduce ambiguity in multi-ecosystem deployments

It does not assert normative authority over the TRQP specification.
