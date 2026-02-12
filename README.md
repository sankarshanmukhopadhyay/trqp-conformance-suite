# TRQP Conformance Test Suite (CTS)

Certification-grade, evidence-first conformance testing for implementations of the **Trust Registry Query Protocol (TRQP)**.

This repository is intentionally designed to support **auditable, reproducible** conformance claims. “HTTP 200” is not conformance. Conformance requires **assertions + evidence**.

---

## What this repo provides

- **Profile-based conformance** (Baseline, Enterprise, High-Assurance)
- **Requirement catalog** with stable IDs mapped to tests
- **Assertion-based test runner** that emits **evidence bundles**
- **Deterministic verdict model**: PASS / FAIL / INCONCLUSIVE / NOT_APPLICABLE
- **Integrity & signing** for evidence manifests (Ed25519)
- **CI-ready** workflows for continuous conformance

---

## Repo layout

```text
.
├── cts/                     # Test runner + evidence packaging
├── profiles/                # Conformance profiles
├── requirements/            # Normative requirement catalog(s)
├── tests/                   # Declarative test cases
├── schemas/                 # JSON schemas for validation
├── spec/                    # Proposed spec text (PR-ready)
├── examples/                # Example SUT + fixtures
├── docs/                    # Architecture, profiles, evidence, governance notes
└── .github/                 # Workflows + issue templates + PR template
```

---

## Quickstart (local)

### 1) Create a venv and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r cts/requirements.txt
```

### 2) Start the example SUT (optional)

```bash
pip install fastapi uvicorn
uvicorn examples.poc_service:app --reload
```

### 3) Run the CTS

Baseline:

```bash
python cts/run.py --profile profiles/baseline.yaml --sut examples/sut.local.yaml --out reports/run-baseline
```

High-Assurance (requires headers; see `examples/sut.local.yaml`):

```bash
python cts/run.py --profile profiles/high_assurance.yaml --sut examples/sut.local.yaml --out reports/run-ha
```

---

## Evidence bundles (certification posture)

Each run produces an evidence directory and a portable bundle:

```text
reports/<run-id>/
  run.json                 # run envelope (who/what/when/profile)
  verdicts.json            # per-test verdicts
  cases/                   # per-test transcripts and assertions
  manifest.json            # hashes of artifacts
  manifest.sig             # Ed25519 signature over manifest.json (HA only)
  bundle.zip               # zipped evidence directory for audit portability
```

High-Assurance **gates** on the presence of a `state_reference` (fixture ID / snapshot hash / signed snapshot reference). If state cannot be pinned, semantics cannot be certified.

---

## Conformance philosophy

See:
- `docs/conformance_philosophy.md`
- `docs/evidence_contract.md`
- `docs/profiles.md`

---

## Versioning

This repository uses **SemVer** for the CTS (`vMAJOR.MINOR.PATCH`). Requirement IDs are stable across patch releases.

See `docs/versioning.md`.

---

## Contributing

- Read `CONTRIBUTING.md`
- Open issues using templates under `.github/ISSUE_TEMPLATE/`
- New tests **must** map to a requirement ID.
- New requirements **must** define expected evidence.

---

## License

Apache-2.0. See `LICENSE`.
