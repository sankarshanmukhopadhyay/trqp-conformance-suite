---
owner: maintainers
last_reviewed: 2026-07-03
tier: 0
---

# Change Intake

CTS changes should be evaluated by their effect on executable conformance and downstream evidence.

## Intake checklist

| Question | Required answer |
|---|---|
| Which requirement changes? | Identify requirement IDs, test IDs, or profile IDs. |
| Which evidence changes? | Name the report, verdict, manifest, case file, signature, or bundle descriptor field. |
| What can be tested? | Provide the CTS command, schema check, or replay command. |
| Who benefits? | Identify implementer, working group, assessor, operator, or Hub consumer. |
| Is a release justified? | Explain why the change is patch, minor, maturity, or no-release. |

## Batching rule

Batch small wording updates, non-normative notes, and internal cross-link cleanup into the next milestone. Cut a release only when the conformance engine, evidence contract, or adopter workflow materially changes.
