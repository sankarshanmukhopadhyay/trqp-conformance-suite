---
layout: default
title: "Conformance assessment and evidence flow"
parent: Architecture
nav_order: 1
---

# Conformance assessment and evidence flow

The suite already contained architecture material, but the assessment lifecycle and its evidence boundary were not represented as a compact implementation-facing decision flow. This diagram links profile selection, execution, remediation, and assurance publication.

```mermaid
flowchart LR
    Implementer[TRQP implementer] --> Profile[Select conformance profile]
    Profile --> Fixture[Load normative fixtures and schemas]
    Fixture --> Runner[Execute conformance test runner]
    Target[System under test] --> Runner
    Runner --> Outcome{All mandatory tests pass?}
    Outcome -- No --> Findings[Emit machine-readable findings]
    Findings --> Remediate[Correct implementation]
    Remediate --> Target
    Outcome -- Yes --> Report[Generate conformance report]
    Report --> Evidence[Package traceable evidence artifacts]
    Evidence --> Hub[Submit to coordinated assurance workflow]
```

## Assurance interpretation

The diagram is normative only where it links to an identified specification, schema, profile, or executable test. Each transition should produce inspectable evidence: selected profile identifiers, test inputs, result artifacts, decision records, and publication manifests. Revocation or supersession must be represented by lifecycle data rather than by silently replacing prior evidence.
