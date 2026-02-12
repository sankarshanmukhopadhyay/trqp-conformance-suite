# Contributing

## Ground rules
1. Every new test **must** map to a requirement ID.
2. Every requirement **must** define expected behavior + required evidence.
3. Avoid ecosystem-specific assumptions unless gated behind a profile.
4. Never treat “request succeeded” as proof of conformance—always attach evidence.

## Workflow
- Open an issue describing the change.
- Submit a PR referencing the issue.
- Ensure CI passes for Baseline + High-Assurance.
- Update docs if evidence format/profile semantics changed.
