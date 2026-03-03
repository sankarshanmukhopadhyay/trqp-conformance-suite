# Changelog


## v0.6.0 (2026-03-03)

- Add **DeDi experimental** artifact validation (vendored schemas + validation script).
- Add `profiles/dedi_experimental.yaml` to enable DeDi profile runs.
- Documentation updates linking DeDi profile to TRQP Assurance Hub experimental mapping.


## v0.6.0 (2026-03-03)

- Add SAD-1 schemas for directory entry, publication manifest, and status feed.
- Add `scripts/validate_directory_artifacts.py` to validate authoritative directory artifacts as evidence (schema validation).
- Add documentation for directory artifact validation and how it complements API conformance testing.

## Unreleased

- Recognize supply chain integrity artifacts (SBOM, provenance, Scorecard) in evidence bundle schema and documentation.
- (nothing yet)
- Add lightweight UNTP DIA context wiring checks to directory artifact validator; vendor DIA JSON-LD context.
## v0.4.4
### Added
- Optional GRID artifact schemas (registrar listing + status feed)
- GRID support documentation with external reference pointers

### Changed
- Documentation crosswalk updated to reference GRID artifacts

## v0.4.1
### Added
- `al-contract.json` to pin Assurance Level semantics to the canonical TRQP Assurance Hub definitions.
- `docs/templates/traceability-template.md` for implementer traceability (explicitly non-normative).

### Changed
- Clarified that this repo consumes canonical AL1–AL4 semantics and does not redefine them.
- Updated documentation to reduce template/template audit noise.

## v0.4.0
### Added
- Conformance suite structure: profiles, requirements, tests, runner scaffolding, and evidence bundle patterns.
