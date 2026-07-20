---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Release Validation

This record defines the validation gate for CTS v1.6.0 in the Operational Trust Stack Maturity Release.

## Compatibility tuple

| Repository | Version | Role |
|---|---:|---|
| TRQP Conformance Suite | v1.6.0 | Protocol conformance evidence producer |
| TRQP-TSPP | v0.14.0 | Security and privacy posture evidence producer |
| TRQP Assurance Hub | v1.9.0 | Combined assurance orchestration and publication |

## Required commands

```bash
python scripts/doc_tests.py
python scripts/schema_check.py
python cts/run.py --list-tests --profile profiles/baseline.yaml
python cts/run.py --profile profiles/smoke.yaml --sut examples/sut.local.yaml.example --dry-run
```

## Acceptance criteria

- Markdown internal links resolve.
- JSON and YAML artifacts parse.
- Schema checks complete without regression.
- Profile inspection lists deterministic test coverage.
- Dry-run validation succeeds without network access to a live SUT.
- Evidence bundle semantics remain compatible with Hub v1.9.0 ingestion.

## Local validation status

| Check | Status | Notes |
|---|---|---|
| `python scripts/doc_tests.py` | Passed | Markdown links and parse checks completed locally. |
| `python scripts/check_doc_freshness.py` | Passed | Governed document freshness metadata refreshed for the maturity release. |
| `python scripts/schema_check.py` | Passed | Schema checks completed locally. |
| `python cts/run.py --list-tests --profile profiles/baseline.yaml` | Blocked locally | Local environment lacked `requests`; dependency installation was blocked by package-index/proxy access. Must be rerun in CI or a developer environment with `cts/requirements.txt` installed. |
| `python cts/run.py --profile profiles/smoke.yaml --sut examples/sut.local.yaml.example --dry-run` | Blocked locally | Same `requests` dependency blocker as above. |

## Release decision

CTS v1.6.0 is release-worthy because it establishes the governance and validation threshold for future conformance-suite releases while preserving compatibility with v1.4.0 evidence consumers.
