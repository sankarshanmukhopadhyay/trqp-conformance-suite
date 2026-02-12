# Conformance philosophy

This CTS is built around four principles:

## 1) Profile-based conformance
TRQP is deployed across assurance environments. Conformance is evaluated against explicit **profiles**.

## 2) Assertion-based testing
Requirements are expressed as testable assertions with:
- Preconditions
- Inputs
- Expected outcomes
- Required evidence artifacts
- Pass/fail rules

## 3) Deterministic verdict model
Each test yields one of:
- PASS
- FAIL
- INCONCLUSIVE
- NOT_APPLICABLE

No silent passes.

## 4) Evidence-first reporting
Every verdict is backed by evidence artifacts:
- Request/response transcripts
- Schema validation outputs
- Semantic checks
- Integrity hashes
- Signed manifest (High-Assurance)
