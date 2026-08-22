# TRQP Conformance Suite v1.8.0

## Deterministic Evidence Replay

This release makes replay determinism a first-class conformance invariant.

### Highlights

- Versioned replay comparison policy with explicit volatile-field allowances.
- Canonical semantic comparison with JSON Pointer-level difference evidence.
- Schema-valid `determinism-report.json` with policy identity, version, SHA-256 provenance, semantic hashes, and permitted/prohibited difference counts.
- Negative tests proving semantic mutations fail while permitted execution metadata changes do not.
- CI determinism gate moved to the fixture-pinned Baseline execution domain.
- Determinism report and comparison policy attached to the fixture Baseline evidence bundle for Assurance Hub consumption.
- Backward-compatible verifier support for legacy verdict-only replay reports.

### Assurance statement

A passing deterministic replay means the replay is evidence-equivalent for conformance-semantic fields under the declared comparison policy. It does not assert that live transport metadata, timing, or run identifiers are byte-identical.

Closes #24.
