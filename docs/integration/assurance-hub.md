# Assurance Hub integration

The Operational Stack baseline expects CTS to emit a machine-readable report that the Assurance Hub can ingest directly.

## Required CTS fields

- `run_id`
- `target_id`
- `profile_id`
- `suite_version`
- `summary`
- `results`

Use `--run-id` and `--target-id` when invoking `cts/run.py` for cross-repo stack runs.

```bash
python cts/run.py   --profile profiles/interop_demo.yaml   --sut examples/sut.local.yaml   --out reports/interop_demo   --run-id opstack-demo-001   --target-id demo-directory
```
