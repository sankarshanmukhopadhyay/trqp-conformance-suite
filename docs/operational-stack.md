---
owner: maintainers
last_reviewed: 2026-04-16
tier: 0
---

# Operational Trust Stack v1

This repository is the verification engine in the Operational Trust Stack v1 release line.

## Role in the stack

The Conformance Suite turns protocol expectations into repeatable evidence artifacts and a machine-readable Conformance Report.

## What is new in v1.2.1

- Conformance Report now includes `coverage_index`
- Evidence completeness is surfaced as an explicit runtime metric
- Golden flow example assets are included for stack integration
- README, Quickstart, and index content are synchronized for public release

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication


## Required identity contract

For combined assurance workflows, the CTS report MUST expose the same `run_id` and `target_id` as the paired TSPP report. The Assurance Hub now treats drift in these fields as a hard validation failure rather than an advisory warning.
