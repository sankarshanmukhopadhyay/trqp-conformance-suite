# Output Contract: CTS Evidence Runs

This document describes the **stable, operator-facing output layout** produced by `cts/run.py`.

It exists to make evidence collection *boring* (repeatable) for adopters and to make automation pipelines easier to build.

## Output directory layout

When you run CTS with `--out <DIR>`, CTS writes the following structure:

```
<DIR>/
  run.json
  verdicts.json
  manifest.json
  manifest.sig            # only if the profile requires signing
  bundle_descriptor.json
  checksums.json
  bundle.zip              # optional, depending on profile evidence settings
  cases/
    <TEST_CASE_ID>.json
```

### Key files

- `run.json` — run metadata (profile id, tool version, timestamps, target base URL metadata)
- `verdicts.json` — flattened verdict list, one entry per test case
- `cases/*.json` — request/response capture + assertions per test case
- `manifest.json` — content hash map of all evidence artifacts in the run (excluding `bundle.zip`)
- `bundle_descriptor.json` — machine-readable index of the bundle’s “entry points”
- `bundle.zip` — convenient packaging of the full run directory (note: deterministic ZIP bytes are handled in Increment 3)

## Determinism controls (Increment 2)

CTS supports deterministic mode so CI pipelines can compare outputs across runs.

- `--run-id <ID>`: override the run identifier.
- `--generated-at <ISO8601>`: override the canonical timestamp used for run metadata.
- `--deterministic`: if set, CTS derives a stable run id (when not provided) and freezes timestamps when `--generated-at` is not provided.
- `--nonce-mode random|derived`: controls HA nonce generation. In deterministic mode, nonces are derived from `(run_id, test_case_id)`.

**Recommended for CI comparisons**

```
python cts/run.py \
  --profile profiles/smoke.yaml \
  --sut sut.example.yaml \
  --out reports/smoke \
  --deterministic \
  --nonce-mode derived
```

For real evidence runs, supply explicit `--run-id` and `--generated-at` so the run is traceable:

```
python cts/run.py ... --run-id 2026-03-02-registryA --generated-at 2026-03-02T00:00:00Z
```
