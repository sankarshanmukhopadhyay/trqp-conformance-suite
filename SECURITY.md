---
layout: default
title: "Security Policy"
nav_exclude: true
---

# Security Policy

## Supported versions

Security fixes are applied to the current `main` branch and the latest supported release line identified by repository status/release metadata. Older releases should be treated as unsupported unless a maintainer explicitly states otherwise.

## Reporting a vulnerability

Do not open public issues for undisclosed vulnerabilities. Use GitHub private vulnerability reporting when available, or contact maintainers through a private channel identified on the maintainer profile. Include the affected component/version, impact, safe reproduction steps, affected evidence, and any suggested remediation.

## Scope

The following areas are in scope for security reports:

- CTS runner logic under `cts/`, especially bugs that can produce false PASS, FAIL, or ERROR verdicts;
- example SUT code under `examples/`, including replay protection, signing, and example credential handling;
- schemas, evidence bundle outputs, and documentation that could mislead implementers or auditors;
- CI workflows and artifact production steps; and
- identifier parameterization logic in `cts/run.py` that maps SUT-supplied values into test bodies.

## Threat model references

Security reports should be interpreted alongside:

- TRQP Assurance Hub `docs/grid-threat-annex.md`;
- TRQP-TSPP `docs/threat-model.md`; and
- `docs/reference/TRACE-TSAM.md`.

## Reporting scope clarification

This repository produces **conformance evidence artifacts**, not production trust decisions. A vulnerability that causes false conformance evidence is in scope because it undermines downstream assurance. Vulnerabilities in downstream registries discovered during CTS runs should be reported to the operator of that registry.

A remediation that changes conformance or reassessment evidence MUST identify affected evidence and MUST NOT silently preserve a stale PASS.

## Related guidance

Read reports alongside `docs/VERIFY_EVIDENCE.md` and the TRQP Assurance Hub combined-assurance documentation.
