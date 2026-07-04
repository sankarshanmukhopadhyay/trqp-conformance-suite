---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Release Policy

The TRQP Conformance Suite is the protocol verification engine for the Operational Trust Stack. Releases should improve executable conformance, evidence portability, interoperability, or adopter confidence.

## Release classes

| Class | Allowed when | Example |
|---|---|---|
| Patch | Security fix, broken CI, broken docs link, schema regression, incorrect release metadata | `v1.5.1` |
| Minor | New executable tests, profile coverage, evidence bundle semantics, replay behavior, or interoperability reporting | `v1.6.0` |
| Maturity | Coordinated CTS, TSPP, and Hub release train | Operational Trust Stack maturity release |
| No release | Typo, prose polish, non-substantive reference refresh | Batch into next milestone |

## Required release evidence

Every release must provide:

- Requirement or profile impact summary.
- Evidence artifact impact summary.
- Validation commands and outcomes.
- Compatibility tuple for CTS, TSPP, and Hub.
- Upgrade note for implementers and downstream assurance consumers.

## Release blockers

A release must not be cut when:

- `VERSION`, README, changelog, release notes, and compatibility references disagree.
- New or changed tests lack documented evidence expectations.
- Schema or example changes are not validated.
- The change is only editorial and does not fix a broken public path or incorrect assurance statement.
