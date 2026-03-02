# GRID support (optional)

CTS can validate the **shape** of GRID-style artifacts (schema validation) to reduce integration risk for directory operators and verifiers.

## What CTS validates

- `registrar.json` against `schemas/registrar.schema.json`
- `grid-status-feed.json` against `schemas/grid-status-feed.schema.json`

## What CTS does not validate (yet)

- Cryptographic signature verification for the status feed
- Evidence sufficiency judgments for AL3/AL4 beyond presence/structure checks

For the operational verifier workflow, see the Assurance Hub:
- `profiles/grid-profile.md`
- `docs/how-to-verify-grid.md`
