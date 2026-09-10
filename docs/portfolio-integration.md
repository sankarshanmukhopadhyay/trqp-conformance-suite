---
layout: default
title: "Portfolio Integration"
nav_exclude: true
permalink: /docs/portfolio-integration/
---

# Portfolio Integration

The TRQP Conformance Suite participates in the coordinated TRQP Operational Trust Stack through `portfolio/integration-contract.json` and the machine-readable producer contract in `portfolio/stack-producer-contract.json`.

## Current coordinated release

**TRQP Stack 2026.3 — Banyan** validates the following adopter-facing tuple:

| Layer | Release |
|---|---:|
| TRQP-TSPP | v0.17.0 |
| TRQP Conformance Suite | v1.10.0 |
| TRQP Assurance Hub | v1.13.0 |
| TSMM | 0.24.0 |
| TIS | 0.15.0 |

The Assurance Hub is the coordinated-release authority and adopter front door. The Stack release declares that this exact tuple passed immutable component resolution, clean bootstrap, component evidence generation, CTS deterministic replay, profile-aware producer/consumer validation, combined-assurance composition, fail-closed negative cases, whole-stack semantic replay equivalence, provenance/integrity checks, and the executable adopter walkthrough.

The coordinated release does **not** replace CTS's independent versioning or authority. CTS remains authoritative for executable conformance requirements, verdict production, evidence bundles, replay-comparison semantics, and its producer-issued profile-consumable conformance evidence.

## Consumer value

An adopter can select the coordinated Stack release without independently determining which CTS version is compatible with the TSPP and Assurance Hub releases. CTS v1.10.0 supplies protocol-conformance, deterministic replay, and profile-consumable core-conformance evidence under declared comparison and lifecycle rules, which the Hub consumes without redefining CTS semantics.

## Repository responsibilities

The Conformance Suite owns executable tests, conformance verdicts, replay-comparison policy, and producer-issued conformance evidence. TRQP-TSPP owns its security/privacy control and posture semantics. Shared semantic definitions are referenced from QBF Consulting's `trust-systems-meta-model` 0.24.0, while shared portable contract/schema authority is referenced from QBF Consulting's `trust-infrastructure-schemas` 0.15.0.

The resulting CTS evidence is combined with TSPP posture evidence and applicable profile/external-authority evidence by the TRQP Assurance Hub for coordinated assurance publication. Profile correlation metadata cannot change CTS core results, and stale or materially affected CTS evidence cannot be promoted to current by a downstream consumer.

## Automated validation

`tools/validate_portfolio_contract.py` checks release pins, upstream authority versions, required local evidence, repository relationships, and invalidation conditions. `.github/workflows/portfolio-contract.yml` runs these checks for pull requests and pushes to `main` and uploads a JSON validation result.

Missing traceability evidence, incompatible authority versions, producer-contract violations, replay-policy incompatibility, or an incompatible normative source invalidates the portfolio integration status.

## Release record

The canonical coordinated release record is maintained by the TRQP Assurance Hub under `stack/releases/2026.3/` and as the GitHub release tag `trqp-stack-2026.3`. Component releases continue to be published independently using repository-local semantic versioning.

Historical Stack 2026.1 and 2026.2 records remain immutable evidence of their tested tuples and are not rewritten when a newer coordinated release becomes current.
