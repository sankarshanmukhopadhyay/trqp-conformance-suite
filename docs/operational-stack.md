---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Operational Trust Stack v1

This repository is the verification engine in the Operational Trust Stack v1 release line.

## Role in the stack

The Conformance Suite turns protocol expectations into repeatable evidence artifacts and a machine-readable Conformance Report.

## Current maturity release

- CTS v1.5.0 is part of the Hub v1.8.0 / CTS v1.5.0 / TSPP v0.13.0 maturity tuple.
- Release governance now distinguishes patch, minor, maturity, and no-release changes.
- Release validation is recorded in `docs/release-validation.md`.
- The CTS evidence contract remains compatible with Hub ingestion while future releases are gated on executable conformance or evidence value.

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication


## Required identity contract

For combined assurance workflows, the CTS report MUST expose the same `run_id` and `target_id` as the paired TSPP report. The Assurance Hub now treats drift in these fields as a hard validation failure rather than an advisory warning.
