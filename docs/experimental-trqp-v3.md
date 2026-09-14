# Experimental TRQP v3 conformance evidence

Status: **experimental downstream evidence; not an adopted Trust Over IP conformance target**.

Tracking issue: https://github.com/sankarshanmukhopadhyay/trqp-conformance-suite/issues/51

Umbrella tranche: https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/55

## Normative target

This branch evaluates the downstream candidate specification at:

- repository: `sankarshanmukhopadhyay/tswg-trust-registry-protocol`
- branch: `draft/next-trqp`
- pinned commit: `532a570ed8b7b468b7a317030077577b9859c14f`
- normative candidate: `specification/v3/TRQP-V3.md`
- stable requirement register: `specification/v3/conformance/REQUIREMENTS.md`

The machine-readable pin is `experimental/trqp-v3/source-pin.json`.

A later candidate commit does not inherit this evidence. The pin must be updated deliberately and the corpus rerun.

## What is tested

`experimental/trqp-v3/vectors.json` carries one executable vector for every release-significant candidate requirement currently identified by the candidate requirement register. The dependency-free oracle in `scripts/validate_v3_candidate.py` verifies:

- exact proposition and decision-critical-context preservation;
- independent principal and verification-material state;
- lifecycle, revocation, expiry, supersession and historical evaluation;
- authority, completeness, freshness, temporal coverage, provenance and conflict in evidence;
- positive, negative, indeterminate and not-applicable decision classes;
- semantic decision separation from transport state;
- negotiation and no-silent-downgrade behaviour;
- binding, discovery, profile and recognition boundaries;
- fail-closed security/privacy cases; and
- audit reconstruction and v2/v3 migration boundaries.

The corpus deliberately includes negative and indeterminate outcomes. A transport/workflow success is never converted into a semantic PASS merely because execution completed.

## Claim boundary

`experimental/trqp-v3/evidence.json` is evidence that the **CTS candidate-v3 semantic oracle and vector corpus** cover and enforce the pinned candidate obligations. It is not evidence that an arbitrary production TRQP implementation conforms to candidate v3.

Production SUT conformance remains a separate claim and should reuse these vectors only after the candidate is promoted or an explicitly experimental SUT profile is selected.

## Run locally

```bash
make v3-candidate-check
```

or:

```bash
python scripts/validate_v3_candidate.py
python -m unittest tests.test_v3_candidate
```

## Promotion rule

This evidence may inform candidate specification revision and Assurance Hub reconciliation. It does not change upstream authority, does not modify stable `main`, and must not be described as adopted TRQP v3 conformance until the relevant authority adopts such a specification.
