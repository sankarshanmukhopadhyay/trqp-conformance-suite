# Profiles

## Baseline

Schema validation, structured errors, deterministic outcomes under stable state.

## Enterprise

Adds governance metadata expectations and operational discipline.

## High-Assurance

Requires declared state reference, replay resistance expectations, and signed evidence bundles.


## AL3 and AL4 alignment (CTS ↔ TSPP)

The Conformance Suite validates **TRQP protocol behavior**. Assurance levels AL1–AL4 are defined by **TRQP‑TSPP**.

For convenience, this repo includes `profiles/al3.yaml` and `profiles/al4.yaml` as **reporting/profile bundles** that:
- reuse the `high_assurance` test set, and
- annotate the run with `assurance_level: AL3` / `AL4` in the evidence bundle.

**Important:** AL3/AL4 *security posture* is asserted and audited in TRQP‑TSPP (metadata + harness), not by CTS alone.
