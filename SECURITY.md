# Security Policy

## Reporting a vulnerability
Do not open public issues for vulnerabilities. Report privately to maintainers with the affected component, impact, safe reproduction steps, and any suggested remediation.

## Scope
The following areas are in scope for security reports:

- CTS runner logic under `cts/`, especially bugs that can produce false PASS, FAIL, or ERROR verdicts
- example SUT code under `examples/`, including replay protection, signing, and example credential handling
- schemas, evidence bundle outputs, and documentation that could mislead implementers or auditors
- CI workflows and artifact production steps

## Related guidance
Read reports alongside `docs/reference/TRACE-TSAM.md`, `docs/VERIFY_EVIDENCE.md`, and the TRQP Assurance Hub threat and assurance documentation.
