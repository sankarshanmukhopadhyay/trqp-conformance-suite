---
owner: maintainers
last_reviewed: 2026-03-17
tier: 0
---

# Operational Trust Stack v1

This repository is the verification engine in the Operational Trust Stack v1 release line.

## Role in the stack

The Conformance Suite turns protocol expectations into repeatable evidence artifacts and a machine-readable Conformance Report.

## What is new in v1.0.0

- Conformance Report now includes `coverage_index`
- Evidence completeness is surfaced as an explicit runtime metric
- Golden flow example assets are included for stack integration
- README, Quickstart, and index content are synchronized for public release

## Golden flow

System under test -> TSPP Posture Report -> Conformance Report -> Combined Assurance Manifest -> Trust Registry publication
