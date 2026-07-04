## v1.5.0

- Publish the CTS portion of the Operational Trust Stack Maturity Release for the coordinated Hub v1.8.0 / CTS v1.5.0 / TSPP v0.13.0 release tuple.
- Add `docs/governance/release-policy.md` to define patch, minor, maturity, and no-release thresholds for the conformance engine.
- Add `docs/governance/change-intake.md` to require requirement impact, profile impact, evidence impact, validation impact, and cross-repo compatibility review.
- Add `docs/release-validation.md` with maturity-release validation commands and acceptance criteria.
- Refresh README and roadmap language to emphasize high-value, evidence-producing CTS commits.
- Align GitHub PR and release templates with the maturity gate.

## v1.4.0

- Add `docs/tis-evidence-contract.md` to map CTS outputs to TIS v0.10.0 evidence and conformance artifact roles.
- Extend evidence bundle descriptor schemas with optional `tis_projection` metadata.
- Add golden-flow TIS-compatible conformance declaration and evidence bundle manifest samples.
- Add portfolio release-impact and drift-review records under `docs/governance/`.
- Refresh README and cross-repo references for Hub v1.7.0 and TSPP v0.12.0.

## v1.3.1

- Add `schemas/lifecycle-status-feed.schema.json` for machine-readable lifecycle and revocation status publication.
- Add CTS test `TC-LIFE-001` for `/.well-known/trqp-lifecycle`, gated to Enterprise and High-Assurance profiles.
- Update the Enterprise profile to include `TRQP-LIFE-001`, making lifecycle/status publication part of adoption-grade conformance evidence.
- Extend the PoC service with a lifecycle/status feed so local implementers can test the new requirement.

## v1.3.0

- Add scenario profiles for ecosystem onboarding, public directories, supply-chain registries, and AI agent service registries.
- Add interop evidence matrix generator, docs, and sample outputs.
- Refresh Hub/TSPP cross-repo references for the coordinated adoption-readiness release.

## v1.2.1

- Refresh README and cross-repo docs for Assurance Hub v1.5.0 and TSPP v0.10.1.
- Make the Operational Stack identity contract explicit: CTS reports participating in a Combined Assurance Manifest must share `run_id` and `target_id` with the paired TSPP report.

## v1.2.0

- Synchronize cross-repo version references to TRQP-TSPP v0.10.0 and trqp-assurance-hub v1.4.0 (Release Set B).
- Update `docs/hub-crosswalk.md` version pins.

## v1.1.0

- Add `--generated-at` flag to `cts/run.py` to pin timestamps for deterministic, reproducible evidence artifacts.
- Add `--fixture-set` flag to `cts/run.py` for canned-response runs without a live SUT; embeds fixture set SHA-256 and ID in `run.json` for full provenance.
- Add `--replay <run-dir>` flag to `cts/run.py` to re-evaluate assertion logic over captured case files without hitting a SUT; emits `replay-report.json` with per-assertion verdict diffs.
- Extract `_evaluate_assertions()` as a shared helper used by both live runs and replay, eliminating assertion logic duplication.
- Add `fixtures/baseline.fixture-set.json`: canonical canned-response fixture set for the baseline profile, covering all 11 non-HA test cases with schema-valid responses.
- Update CI workflow to run the fixture-pinned baseline profile deterministically on every push, and to replay the live baseline run as a post-run determinism check.
- Fix `docs/assurance-levels.canonical.md` back-link (`./index.md` → `../index.md`) to resolve correctly from the `docs/` subdirectory.
- Update `al-contract.json` to pin the corrected canonical doc SHA-256 (`61c599c5...`) matching TRQP Assurance Hub v1.2.0 and TRQP-TSPP v0.8.0.

## v1.0.0

- Added coverage and evidence completeness metrics to the Conformance Report.
- Added Operational Trust Stack public documentation and Golden Flow examples.
- Refreshed public-facing docs and synchronized versions across the stack.

## v0.9.0

- Add an `interop_demo` profile for onboarding and Operational Stack demonstrations.
- Extend `cts/run.py` with shared `--run-id` and `--target-id` support and emit `cts-report.json` for Assurance Hub ingestion.
- Add `docs/integration/assurance-hub.md` to document the integrated workflow.

# Changelog

## v0.8.0 (2026-03-10)

### Fixed
- Rename `recognised`/`recognised_since` → `recognized`/`recognized_since` in `schemas/core/recog_response.schema.json` and `examples/poc_service.py` to align with ToIP TRQP v2.0 specification and TSPP. UK/US spelling divergence meant a server passing CTS would use the wrong field names against the TSPP harness and the Ayra TRQP Profile API.
- Fix broken internal link in `docs/assurance-levels.canonical.md` (`../index.md` → `./index.md`). The previous link resolved to the repo root, which has no `index.md`.
- Align `docs/hub-crosswalk.md` version pins with `al-contract.json`: Assurance Hub v0.8.1 → v0.9.0; CTS v0.7.1 → v0.8.0; TSPP v0.5.1 → v0.6.0.

### Added
- Add optional `meta` object (`time_evaluated`, `expires_at`) to `schemas/core/authz_response.schema.json` and `schemas/core/recog_response.schema.json`. Servers conforming to TSPP AL1+ must emit these fields; CTS now accepts and validates them.
- Add `meta` freshness envelope to `examples/poc_service.py` authorization and recognition responses, making the reference SUT passable against both CTS and the TSPP AL1 harness without reconfiguration.
- Add TRQP-FRESH-001 and TRQP-FRESH-002 (SHOULD-level) requirements with tests TC-FRESH-001/002 checking `meta.time_evaluated` and `meta.expires_at`. Gated under Enterprise profile.
- Strengthen `schemas/core/error.schema.json` with a stable `error` enum aligned with the TSPP error surface and an optional `meta.time_evaluated` field.
- Add `profiles/ayra_baseline.yaml`: Ayra Trust Network TRQP pre-certification profile extending Enterprise.
- Add `docs/ayra-crosswalk.md`: crosswalk from CTS/TSPP evidence artifacts to Ayra conformance requirements.
- Add frontmatter to `docs/hub-crosswalk.md` for freshness SLA enforcement.

### Changed
- Update `profiles/enterprise.yaml` to include TRQP-FRESH-001 and TRQP-FRESH-002.
- Update `examples/poc_service.py` `_freshness_meta()` helper to produce deterministic freshness envelopes.

## Cross-repo versions

| Repository | Version |
|---|---|
| TRQP-TSPP | v0.6.0 |
| Conformance Suite | v0.8.0 |
| Assurance Hub | v0.9.0 |

## v0.7.1 (2026-03-06)

- Synchronize public-facing documentation and release metadata with TRQP-TSPP v0.5.1 and Assurance Hub v0.8.1.
- Retain Commit 3 and 4 tooling additions while removing stale version drift from README, roadmap, and crosswalk docs.
- Refresh release artifacts for the coordinated patch alignment release.

## v0.3.0 (2026-03-06)

### Added
- Add `--dry-run` flag to `cts/run.py` to validate inputs and list applicable tests without making HTTP requests.
- Add `--list-tests` flag to `cts/run.py` to print tests applicable to the selected profile and exit.
- Add `identifiers` block support to `sut.yaml` config, allowing real SUTs to override `authority_id`, `entity_id`, `subject_authority_id`, and `action` without modifying core test definitions.
- Add `QUICKSTART.md` at the repository root for fast onboarding of new implementers and operators.

### Fixed
- Fix JSONPath wildcard token indexing bug: `tokens.index(tok)` was replaced with `enumerate`-based tracking, preventing incorrect remainder slicing when a wildcard token appeared more than once in a path.

### Changed
- Refactor `cts/run.py` to extract `resolve_identifiers`, `apply_identifier_overrides`, and `list_tests` functions, reducing the size of `main()` and making each concern independently testable.
- Update `examples/sut.local.yaml.example` to document the `identifiers:` override block.
- Expand `SECURITY.md` with threat model references and reporting scope clarification.
- Synchronize roadmap, release notes, and version pins for the coordinated v0.3.0 release.

---

*Prior entries below reflect earlier releases in this series.*

## v0.7.0 (2026-03-06)

- Add machine-verifiable AL contract pin checking using a canonical assurance-level snapshot from the Assurance Hub.
- Synchronize cross-repo version references and public-facing release documentation for the AL3/AL4 hardening release train.

## v0.6.1 (2026-03-06)

### Fixed
- Reset per-test verdict override state in `cts/run.py` so an earlier ERROR does not leak into later passing cases.
- Write `checksums.json.generated_at` with a real timestamp instead of a null value.
- Synchronize README, roadmap, security guidance, and version pins for the current patch release.

### Changed
- Move the example SUT configuration to `examples/sut.local.yaml.example` and require generated local signing keys.
- Add explicit security warnings to the PoC service and example SUT configuration.
- Replace the placeholder GitHub Pages URL in the README with the production repository URL.

### Added
- Extend `.gitignore` to keep generated local SUT configs out of version control.

## v0.6.0 (2026-03-03)

### Added
- DeDi experimental artifact validation (vendored schemas plus validation script).
- `profiles/dedi_experimental.yaml` to enable DeDi profile runs.
- SAD-1 schemas for directory entry, publication manifest, and status feed.
- `scripts/validate_directory_artifacts.py` to validate authoritative directory artifacts as evidence.
- Documentation for directory artifact validation and how it complements API conformance testing.

### Changed
- Documentation updates linking DeDi profile to TRQP Assurance Hub experimental mapping.

## v0.4.4

### Added
- Optional GRID artifact schemas (registrar listing and status feed).
- GRID support documentation with external reference pointers.

### Changed
- Documentation crosswalk updated to reference GRID artifacts.

## v0.4.1

### Added
- `al-contract.json` to pin Assurance Level semantics to the canonical TRQP Assurance Hub definitions.
- `docs/templates/traceability-template.md` for implementer traceability (explicitly non-normative).

### Changed
- Clarified that this repo consumes canonical AL1 to AL4 semantics and does not redefine them.
- Updated documentation to reduce template noise.

## v0.4.0

### Added
- Conformance suite structure: profiles, requirements, tests, runner scaffolding, and evidence bundle patterns.
