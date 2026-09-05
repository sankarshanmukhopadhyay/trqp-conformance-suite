---
layout: default
title: Public repository baseline
nav_exclude: true
---

# Public repository baseline

This record captures the controls reviewed under issue #37. It is repository assurance evidence, not external certification.

| Control | State | Evidence | Residual risk |
|---|---|---|---|
| Purpose, maturity and adopter path | PASS | `README.md`, `QUICKSTART.md`, `PROJECT-STATUS.yaml` | None identified. |
| Licensing | PASS | `LICENSE`, `NOTICE` | None identified. |
| Security reporting and supported versions | PASS | `SECURITY.md` | Hosted private-vulnerability-reporting enablement remains platform evidence. |
| Contribution/community/support guidance | PASS | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, issue/PR templates | None identified. |
| Dependency update management | PASS | `.github/dependabot.yml`, `.github/DEPENDABOT_AUTOMERGE.md` | Hosted Dependabot enablement remains platform evidence. |
| Default-branch governance | PASS | active `protect-main` observed 2026-09-05: PRs, conversation resolution, linear history, delete/non-fast-forward protection, strict `validate` + `validate-reassessment`, no bypass actors | Required check names must remain synchronized with CI. |
| Conformance/reassessment evidence | PASS | CTS test/replay/reassessment machinery and required checks | Workflow green is evidence, not a production trust decision. |
| Release/version provenance | PASS | `CHANGELOG.md`, `CITATION.cff`, release template/status surfaces | Publication remains maintainer judgment. |
| Authority boundary | PASS | `GOVERNANCE.md`, README/docs | CTS owns conformance/replay consequences, not upstream materiality or downstream combined assurance. |

## Completion boundary

The applicable public-repository baseline is complete when the associated remediation PR merges with required checks green. Hosted GitHub security-feature enablement is not inferred from repository files.
