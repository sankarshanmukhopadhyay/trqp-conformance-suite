---
layout: default
title: "TRQP Stack producer contract"
nav_exclude: true
---

# TRQP Stack producer contract

The TRQP Conformance Suite is the protocol-conformance and replay-evidence producer for coordinated TRQP Operational Trust Stack releases. Its machine-readable stack boundary is declared in `portfolio/stack-producer-contract.json`.

The contract requires conformance evidence, replay-determinism evidence, and the replay comparison-policy identity to be consumable by the TRQP Assurance Hub. Cross-stack evidence must share `run_id` and `target_id`; coordinated releases must preserve component provenance and artifact integrity hashes.

CTS remains authoritative for protocol-conformance execution, CTS evidence semantics, replay comparison policy, and replay-determinism verdicts. The contract does not transfer authority over TSPP controls, combined assurance decisions, or coordinated stack-release declarations.

Consumers must fail closed on missing/schema-invalid evidence, correlation mismatch, failed replay determinism, an unrecognised comparison policy, or an unsupported semantic/schema authority tuple.
