# Start Here

Before diving into mechanics, read the cross-repo program narrative: [Program playbook](PLAYBOOK.md).


This repository provides a conformance testing approach for TRQP with profile-based assurance and evidence bundles.

---

## Implementing TRQP

1. Run the **Baseline** profile.
2. Review `reports/<run-id>/verdicts.json` for requirement-level failures.
3. Compare your evidence outputs to `docs/reference-reports/`.
4. Move to **High-Assurance** only after you can provide a stable `state_reference`.

---

## Spec authors and working groups

1. Review `docs/TRQP_Conformance_Philosophy.md`.
2. Review `docs/profiles.md`.
3. Use the WG Alignment issue template to propose clarifications and profile gating changes.

---

## Governance and assurance teams

1. Review `docs/evidence_bundle.schema.json`.
2. Inspect reference reports for expected artifact completeness.
3. Validate that a High-Assurance run includes a declared `state_reference`.


## Deterministic mode (Increment 2)

For CI comparisons or repeated runs, CTS supports a deterministic mode:

```bash
python cts/run.py --profile profiles/smoke.yaml --sut sut.example.yaml --out reports/smoke --deterministic --nonce-mode derived
```

See: [docs/OUTPUT_CONTRACT.md](OUTPUT_CONTRACT.md)
