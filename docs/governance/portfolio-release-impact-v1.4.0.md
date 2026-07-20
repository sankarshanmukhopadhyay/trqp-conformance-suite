---
layout: default
title: "Portfolio Release Impact: TRQP Conformance Suite v1.4.0"
nav_exclude: true
---

# Portfolio Release Impact: TRQP Conformance Suite v1.4.0

| Field | Value |
|---|---|
| Repository | `trqp-conformance-suite` |
| Release version | v1.4.0 |
| Release date | 2026-06-29 |
| Primary change type | Evidence artifact contract alignment |
| Portfolio impact classification | Artifact / Assurance / Documentation |

## Changed surfaces

- [x] Schema or runtime artifact
- [x] Evidence bundle or decision receipt
- [x] Conformance verdict or test fixture
- [x] README, onboarding, or adoption workflow

## Relationship review

| Source repo | Target repo | Relationship | Impact | Evidence |
|---|---|---|---|---|
| `trqp-conformance-suite` | `trqp-assurance-hub` | `produces_evidence_for` | CTS evidence descriptors now expose TIS projection metadata | `schemas/evidence/bundle_descriptor.schema.json` |
| `trust-infrastructure-schemas` | `trqp-conformance-suite` | `informs` | CTS documents how output maps to TIS evidence and conformance artifacts | `docs/tis-evidence-contract.md` |
| `trust-systems-meta-model` | `trqp-conformance-suite` | `informs` | CTS clarifies authority and scope boundaries for conformance evidence | `docs/tis-evidence-contract.md` |

## Validation evidence

```text
python scripts/schema_check.py
python scripts/doc_tests.py
```

## Decision

- [ ] Release has no cross-repo impact.
- [ ] Release has documentation impact only.
- [x] Release requires downstream artifact/profile/test updates.
- [ ] Release should be held until downstream compatibility is updated.

