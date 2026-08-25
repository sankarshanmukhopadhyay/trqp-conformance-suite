---
layout: default
title: "Portfolio Integration"
nav_exclude: true
permalink: /docs/portfolio-integration/
---

# Portfolio Integration

The TRQP Conformance Suite participates in the coordinated TRQP Operational Trust Stack through `portfolio/integration-contract.json` and the machine-readable producer contract in `portfolio/stack-producer-contract.json`.

## Current coordinated release

**TRQP Stack 2026.1 — Coconut** validates the following adopter-facing tuple:

| Layer | Release |
|---|---:|
| TRQP-TSPP | v0.15.0 |
| TRQP Conformance Suite | v1.8.0 |
| TRQP Assurance Hub | v1.11.0 |
| TSMM | v0.24.0 |
| TIS | v0.14.1 |

The Assurance Hub is the coordinated-release authority and adopter front door. The Stack release declares that this exact tuple has passed clean bootstrap, component evidence generation, CTS deterministic replay, combined-assurance validation, fail-closed negative cases, whole-stack semantic replay equivalence, provenance/integrity checks, and the executable adopter walkthrough.

The coordinated release does **not** replace CTS's independent versioning or authority. CTS remains authoritative for executable conformance requirements, verdict production, evidence bundles, and replay-comparison semantics.

## Consumer value

An adopter can select the coordinated Stack release without independently determining which CTS version is compatible with the TSPP and Assurance Hub releases. CTS v1.8.0 supplies protocol-conformance and deterministic replay evidence under a declared comparison policy, which the Hub consumes without redefining CTS semantics.

## Repository responsibilities

The Conformance Suite owns executable tests, conformance verdicts, replay-comparison policy, and producer-issued conformance evidence. TRQP-TSPP owns its security/privacy control and posture semantics. Shared semantic definitions are referenced from `trust-systems-meta-model` v0.24.0, while shared portfolio and repository schemas are referenced from `trust-infrastructure-schemas` v0.14.1.

The resulting CTS evidence is combined with TSPP posture evidence by the TRQP Assurance Hub for coordinated assurance publication.

## Automated validation

`tools/validate_portfolio_contract.py` checks release pins, upstream authority versions, required local evidence, repository relationships, and invalidation conditions. `.github/workflows/portfolio-contract.yml` runs these checks for pull requests and pushes to `main` and uploads a JSON validation result.

Missing traceability evidence, incompatible authority versions, producer-contract violations, replay-policy incompatibility, or an incompatible normative source invalidates the portfolio integration status.

## Release record

The canonical coordinated release record is maintained by the TRQP Assurance Hub under `stack/releases/2026.1/`. Component releases continue to be published independently using repository-local semantic versioning.
