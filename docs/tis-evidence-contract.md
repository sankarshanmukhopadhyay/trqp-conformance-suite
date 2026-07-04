---
owner: maintainers
last_reviewed: 2026-06-29
tier: 1
---

# TIS Evidence Contract

TRQP Conformance Suite v1.5.0 maps conformance evidence to Trust Infrastructure Schemas v0.10.0 without making TIS a runtime dependency.

CTS remains responsible for protocol verification. TIS provides artifact contracts that downstream assurance tooling can use to package, reference, and audit CTS outputs.

## Contract mapping

| CTS output | TIS artifact role | Purpose |
|---|---|---|
| `run.json` | conformance run metadata | Records target, profile, tool version, timing, and execution identity |
| `verdicts.json` | conformance verdict evidence | Records assertion outcomes and reasons |
| `manifest.json` | evidence bundle manifest input | Records artifacts produced by the run |
| `checksums.json` | integrity metadata | Provides artifact hashes for audit and replay |
| `cases/*.json` | evidence artifact | Stores request/response transcripts or fixture-derived case evidence |
| `bundle_descriptor.json` | evidence index | Provides the normalized index consumed by Hub and TIS projection workflows |

## Authority, delegation, and scope

CTS does not decide ecosystem authority. It verifies protocol behavior for a declared target and profile. Authority and delegation are therefore represented as scoped metadata:

| Surface | Meaning |
|---|---|
| `run_id` | Shared execution identity for a combined assurance run |
| `target_id` | Stable identifier for the evaluated implementation or service |
| `profile_id` | Conformance scope selected for evaluation |
| `sut` | System under test and state reference |

The Assurance Hub consumes these fields and binds them to authority, lifecycle, and relying-party effects.

## TIS projection metadata

Evidence bundle descriptors MAY include:

```json
{
  "tis_projection": {
    "tis_version": "v0.10.0",
    "evidence_bundle_manifest_schema": "trust-infrastructure-schemas/evidence/evidence-bundle-manifest.schema.json",
    "conformance_declaration_schema": "trust-infrastructure-schemas/conformance/conformance-declaration.schema.json",
    "decision_receipt_schema": "trust-infrastructure-schemas/decision/decision-receipt.schema.json",
    "projected_artifacts": [
      {
        "source_artifact": "verdicts.json",
        "tis_role": "conformance-verdict-evidence"
      }
    ]
  }
}
```

This block tells downstream tooling how to interpret CTS output. It does not claim that CTS has performed certification.

## Enforcement and revocation

CTS validates lifecycle/status publication where the selected profile requires it. It does not enforce revocation itself. Revocation-sensitive reliance requires:

- CTS lifecycle/status feed checks;
- TSPP lifecycle publication posture checks;
- Hub lifecycle fields in the Combined Assurance Manifest;
- optional TIS status or revocation evidence references.

## Audit evidence

For audit-ready use, preserve:

- complete evidence bundle directory;
- `bundle_descriptor.json`;
- `checksums.json`;
- `manifest.json`;
- `verdicts.json`;
- case files;
- signature artifacts where the selected profile produces them.

## Golden flow samples

Sample TIS-compatible artifacts are published in:

- `examples/golden-flow/tis-conformance-declaration.sample.json`
- `examples/golden-flow/tis-evidence-bundle-manifest.sample.json`
