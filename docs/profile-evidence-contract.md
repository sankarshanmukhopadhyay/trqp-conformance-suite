---
owner: maintainers
last_reviewed: 2026-09-10
tier: 1
---

# Profile-consumable CTS evidence

CTS remains authoritative for executable TRQP protocol-conformance and replay evidence. A profile-aware consumer may correlate that evidence to a named ecosystem profile, but profile metadata does not modify CTS core semantics.

The machine-readable contract is `schemas/evidence/profile-consumable-conformance.schema.json`. The export helper is `scripts/build_profile_consumable_evidence.py`.

## Responsibility boundary

| Concern | Authority |
|---|---|
| TRQP core/binding conformance | CTS |
| Replay determinism and reassessment consequence | CTS |
| Ecosystem-profile requirements and extensions | Profile authority, projected by Assurance Hub |
| Security/privacy posture | TRQP-TSPP |
| Governance legitimacy and external authority facts | Applicable external authority/evidence source |
| Cross-source composition and profile assurance publication | TRQP Assurance Hub |

## Producer contract

A profile-consumable artifact records the CTS suite version, exact test-set revision, TRQP protocol version and binding, run and target identity, test-level results, evidence references, and lifecycle/reassessment state.

`profile_context` is correlation metadata only. Two profile consumers may reuse the same current CTS evidence when their core-TRQP applicability is identical; neither profile may alter the underlying CTS results.

Operational `ERROR`, skipped, or otherwise unresolved execution states are exported as `INDETERMINATE`. They are never converted into semantic negative authorization or recognition decisions.

## Reassessment

The producer carries the lifecycle outcome established by the CTS reassessment model. A consumer must not treat `REASSESS_REQUIRED` or `INVALID` evidence as current merely because its profile identifier matches.

Unknown applicability fails safe. If CTS cannot establish that a bounded prior result remains applicable, the existing full-rerun rule remains authoritative.
