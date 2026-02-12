# Evidence contract

## Required artifacts (all profiles)
- `run.json`: run envelope (profile, tool version, SUT endpoint, timestamps)
- `verdicts.json`: per-test results and rationale
- `cases/<case-id>.json`: test transcript + assertion results
- `manifest.json`: cryptographic hashes (sha256) of all artifacts

## High-Assurance additions
- `manifest.sig`: Ed25519 signature over `manifest.json`
- `bundle.zip`: portable evidence bundle

## State determinism
Certification-grade semantics require a **state reference** (fixture set ID / snapshot hash / signed snapshot identifier). Without a state reference, High-Assurance runs are blocked.
