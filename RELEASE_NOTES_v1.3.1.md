# TRQP Conformance Suite v1.3.1 Release Notes

## Summary

This patch adds executable conformance coverage for lifecycle/status publication. Enterprise and High-Assurance runs can now validate that a registry exposes a machine-readable lifecycle feed suitable for suspension, retirement, and revocation decisions.

## Added

- `schemas/lifecycle-status-feed.schema.json`.
- `TC-LIFE-001` for `GET /.well-known/trqp-lifecycle`.
- Enterprise profile requirement `TRQP-LIFE-001`.
- PoC service lifecycle/status feed for local testing.

## Validation

- `python scripts/doc_tests.py`
- `python scripts/schema_check.py`
- Direct YAML/JSON wiring check for `TC-LIFE-001` and `TRQP-LIFE-001`.

## Coordinated Release Tuple

- TRQP-TSPP: v0.11.1
- TRQP Conformance Suite: v1.3.1
- TRQP Assurance Hub: v1.6.1
