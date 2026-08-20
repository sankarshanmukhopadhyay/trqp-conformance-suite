# TRQP Conformance Suite v1.7.0

## Portfolio integration release

This release connects the Conformance Suite to the current executable governance layer provided by Trust Systems Meta-Model v0.24.0 and Trust Infrastructure Schemas v0.14.1.

### Added

- Machine-readable cross-repository integration contract.
- Explicit semantic and schema version pins.
- Declared testing relationship to TRQP-TSPP and evidence relationship to the TRQP Assurance Hub.
- Automated validation of release pins, evidence availability, repository relationships, and invalidation conditions.
- CI-generated portfolio integration evidence artifact.

### Conformance impact

The suite now verifies that its cross-repository role remains bound to the current normative and semantic sources. Missing traceability evidence or incompatible upstream contracts invalidate the integration status.

### Compatibility

Existing conformance profiles and report formats remain compatible. This release adds governance and validation around their cross-repository interpretation.
