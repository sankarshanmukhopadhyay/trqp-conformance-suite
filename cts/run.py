"""CTS runner entrypoint.

This module executes TRQP Conformance Suite profiles against a target SUT and emits
machine-readable evidence artifacts (reports, manifests, bundles).

Operator notes:
- Prefer deterministic mode for CI and audit-grade runs.
- Use --generated-at to pin timestamps for reproducible output.
- Use --fixture-set to run against canned responses instead of a live SUT.
- Use --replay to re-evaluate assertion logic over a prior run directory.
- Outputs are written under the configured output directory with stable naming.

This docstring exists to make the runner easier to maintain and safer to adapt.
"""

import argparse, json, time, hashlib, zipfile, uuid
from pathlib import Path
from datetime import datetime, timezone
import yaml
import requests
from jsonschema import validate as js_validate
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder

ROOT = Path(__file__).resolve().parent.parent
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())

def guess_media_type(p: Path) -> str | None:
    suf = p.suffix.lower()
    if suf == ".json":
        return "application/json"
    if suf == ".zip":
        return "application/zip"
    if suf in [".txt", ".log"]:
        return "text/plain"
    if suf in [".yaml", ".yml"]:
        return "text/yaml"
    return None

def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def json_path_get(doc, path: str):
    """
    Minimal JSONPath-like accessor.

    Supports:
      - $.a.b.c
      - $.a[0].b
      - $["key.with.dots"].a
      - wildcard array iteration: $.items[*].id  (returns list of matches)
    """
    if not path.startswith("$"):
        raise ValueError("Only supports paths starting with $")

    i = 1
    tokens = []
    while i < len(path):
        if path[i] == ".":
            i += 1
            j = i
            while j < len(path) and path[j] not in ".[":
                j += 1
            tokens.append(("key", path[i:j]))
            i = j
        elif path[i] == "[":
            j = path.find("]", i)
            if j == -1:
                raise ValueError(f"Unclosed [ in path: {path}")
            inner = path[i+1:j]
            if inner == "*":
                tokens.append(("wildcard", None))
            elif (inner.startswith('"') and inner.endswith('"')) or (inner.startswith("'") and inner.endswith("'")):
                tokens.append(("key", inner[1:-1]))
            else:
                tokens.append(("index", int(inner)))
            i = j + 1
        else:
            raise ValueError(f"Unexpected character in path at {i}: {path[i]} ({path})")

    def step(cur, tok):
        kind, val = tok
        if kind == "key":
            return cur.get(val) if isinstance(cur, dict) else None
        if kind == "index":
            if isinstance(cur, list) and 0 <= val < len(cur):
                return cur[val]
            return None
        if kind == "wildcard":
            if isinstance(cur, list):
                return cur[:]
            return None
        raise ValueError("unknown token")

    cur = doc
    for idx, tok in enumerate(tokens):
        if tok[0] == "wildcard":
            remainder = tokens[idx + 1:]
            arr = step(cur, tok)
            if arr is None:
                return None
            out = []
            for item in arr:
                c = item
                for rt in remainder:
                    c = step(c, rt)
                    if c is None:
                        break
                if c is not None:
                    out.append(c)
            return out
        else:
            cur = step(cur, tok)
            if cur is None:
                return None
    return cur

def ensure_dirs(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    (out/"cases").mkdir(exist_ok=True)

def http_request(base_url: str, tc: dict, headers: dict, body):
    url = base_url.rstrip("/") + tc["path"]
    method = tc.get("method", "POST").upper()
    return requests.request(method, url, headers=headers, json=body, timeout=20)

def add_ha_headers(headers: dict, sut: dict, nonce: str, ts: str):
    headers["X-Auth-Mode"] = "high_assurance"
    api_key = sut.get("api_key")
    if not api_key:
        raise SystemExit("High assurance profile requires sut.api_key (refusing to default to demo-secret)")
    headers["X-API-Key"] = api_key
    headers["X-Nonce"] = nonce
    headers["X-Timestamp"] = ts

def resolve_identifiers(sut: dict) -> dict:
    """Return identifier overrides from sut config, with defaults."""
    defaults = {
        "authority_id": "did:example:transport-ministry",
        "entity_id": "did:example:logistics-sp-123",
        "subject_authority_id": "did:example:foreign-authority-xyz",
        "action": "issue-transport-credential",
    }
    overrides = sut.get("identifiers", {}) or {}
    return {**defaults, **overrides}

def apply_identifier_overrides(body: dict | None, identifiers: dict) -> dict | None:
    """Replace placeholder identifier values in a request body with SUT-specific overrides."""
    if body is None:
        return body
    result = dict(body)
    for field in ("authority_id", "entity_id", "subject_authority_id", "action"):
        if field in result:
            result[field] = identifiers[field]
    return result

def list_tests(tests: list, profile: dict) -> None:
    """Print test IDs and names applicable to the given profile."""
    profile_id = profile.get("id")
    print(f"Tests applicable to profile '{profile_id}':\n")
    for tc in tests:
        applicable_profiles = tc.get("profiles")
        if applicable_profiles and profile_id not in applicable_profiles:
            status = "NOT_APPLICABLE"
        else:
            status = "applicable"
        print(f"  [{status}] {tc['id']}: {tc.get('name', '')}")
    print()

# ---------------------------------------------------------------------------
# Fixture-set support
# ---------------------------------------------------------------------------

def load_fixture_set(path: Path) -> dict:
    """Load a fixture set JSON file.

    Expected shape::

        {
          "fixture_set_id": "v1",
          "description": "...",
          "fixtures": {
            "<tc_id>": {
              "status": 200,
              "headers": {"Content-Type": "application/json"},
              "body": { ... }
            }
          }
        }
    """
    raw = json.loads(path.read_text(encoding="utf-8"))
    if "fixtures" not in raw:
        raise SystemExit(f"fixture-set file missing 'fixtures' key: {path}")
    return raw


class _FixtureResponse:
    """Minimal stand-in for a requests.Response, backed by a fixture entry."""

    def __init__(self, entry: dict):
        self.status_code: int = int(entry.get("status", 200))
        self.headers: dict = {k: v for k, v in (entry.get("headers") or {}).items()}
        self._body = entry.get("body")
        self.text: str = json.dumps(self._body) if self._body is not None else entry.get("text", "")

    def json(self):
        if self._body is not None:
            return self._body
        return json.loads(self.text)


def fixture_request(fixture_set: dict, tc_id: str):
    """Return a _FixtureResponse for tc_id if present, else None."""
    entry = fixture_set.get("fixtures", {}).get(tc_id)
    if entry is None:
        return None
    return _FixtureResponse(entry)


# ---------------------------------------------------------------------------
# Assertion re-evaluation (shared by live runs and replay)
# ---------------------------------------------------------------------------

def _evaluate_assertions(tc: dict, resp_status, resp_headers: dict, resp_json, resp_text: str) -> tuple[bool, list]:
    """Run all expect-block assertions against response data. Returns (ok, assertions)."""
    ok = True
    assertions = []
    exp = tc.get("expect", {})

    if "status" in exp and "status_in" in exp:
        ok = False
        assertions.append({"type": "expect_config", "error": "expect.status and expect.status_in are mutually exclusive", "pass": False})

    if "status" in exp:
        passed = resp_status == exp["status"]
        ok &= passed
        assertions.append({"type": "status", "expected": exp["status"], "actual": resp_status, "pass": passed})

    if "status_in" in exp:
        passed = resp_status in exp["status_in"]
        ok &= passed
        assertions.append({"type": "status_in", "expected": exp["status_in"], "actual": resp_status, "pass": passed})

    needs_json = any(k in exp for k in ["schema", "json_path_exists", "json_path_equals"]) or exp.get("response_json")
    if needs_json:
        if resp_json is not None:
            assertions.append({"type": "json_parse", "pass": True})
        else:
            try:
                resp_json = json.loads(resp_text) if resp_text else None
                parse_ok = resp_json is not None
            except Exception:
                parse_ok = False
                resp_json = None
            assertions.append({"type": "json_parse", "pass": parse_ok})
            if not parse_ok:
                ok = False

    if "response_header_contains" in exp:
        for k, v in exp["response_header_contains"].items():
            actual = resp_headers.get(k)
            passed = (actual is not None and v in actual) if k.lower() == "content-type" else (actual == v)
            ok &= passed
            assertions.append({"type": "header_contains", "header": k, "expected": v, "actual": actual, "pass": passed})

    if exp.get("schema") and resp_json is not None:
        schema = load_json(ROOT / exp["schema"])
        try:
            js_validate(instance=resp_json, schema=schema)
            assertions.append({"type": "schema", "schema": exp["schema"], "pass": True})
        except Exception as e:
            ok = False
            assertions.append({"type": "schema", "schema": exp["schema"], "pass": False, "error": str(e)})

    if exp.get("json_path_exists") and resp_json is not None:
        for p in exp["json_path_exists"]:
            v = json_path_get(resp_json, p)
            passed = (v is not None) and (v != [])
            ok &= passed
            assertions.append({"type": "json_path_exists", "path": p, "pass": passed})

    if exp.get("json_path_equals") and resp_json is not None:
        for p, expected in exp["json_path_equals"]:
            actual = json_path_get(resp_json, p)
            passed = (actual == expected)
            ok &= passed
            assertions.append({"type": "json_path_equals", "path": p, "expected": expected, "actual": actual, "pass": passed})

    if exp.get("json_path_in") and resp_json is not None:
        for p, allowed in exp["json_path_in"]:
            actual = json_path_get(resp_json, p)
            passed = actual in allowed
            ok &= passed
            assertions.append({"type": "json_path_in", "path": p, "allowed": allowed, "actual": actual, "pass": passed})

    return ok, assertions


# ---------------------------------------------------------------------------
# Replay mode
# ---------------------------------------------------------------------------

def run_replay(replay_dir: Path, out: Path, profile: dict, generated_at: str) -> None:
    """Re-evaluate assertion logic over a prior run directory without hitting a SUT.

    Reads case files from ``replay_dir/cases/*.json``, re-runs all assertion
    checks against the captured response, and emits a ``replay-report.json``
    with per-assertion diffs against the original verdicts.
    """
    cases_dir = replay_dir / "cases"
    if not cases_dir.exists():
        raise SystemExit(f"Replay directory has no cases/ subdirectory: {replay_dir}")

    orig_verdicts_path = replay_dir / "verdicts.json"
    if orig_verdicts_path.exists():
        orig_verdicts = {v["test_case_id"]: v for v in json.loads(orig_verdicts_path.read_text(encoding="utf-8"))}
    else:
        orig_verdicts = {}

    orig_run_path = replay_dir / "run.json"
    orig_run_id = None
    if orig_run_path.exists():
        orig_run = json.loads(orig_run_path.read_text(encoding="utf-8"))
        orig_run_id = orig_run.get("test_run_id")

    out.mkdir(parents=True, exist_ok=True)

    replay_id = str(uuid.uuid4())
    tests = load_yaml(ROOT / "tests/core_tests.yaml")["tests"]
    tests_by_id = {tc["id"]: tc for tc in tests}

    replay_verdicts = []
    diffs = []

    for case_file in sorted(cases_dir.glob("*.json")):
        tc_id = case_file.stem
        case = json.loads(case_file.read_text(encoding="utf-8"))
        tc = tests_by_id.get(tc_id)

        if case.get("skipped"):
            replay_verdicts.append({"test_case_id": tc_id, "result": "NOT_APPLICABLE", "source": "replay"})
            continue

        if tc is None:
            replay_verdicts.append({
                "test_case_id": tc_id,
                "result": "STALE",
                "reason": "test case not found in current suite",
                "source": "replay",
            })
            continue

        resp_status = case.get("response", {}).get("status")
        resp_headers = case.get("response", {}).get("headers", {})
        resp_json = case.get("response", {}).get("json")
        resp_text = case.get("response", {}).get("text", "")

        ok, assertions = _evaluate_assertions(tc, resp_status, resp_headers, resp_json, resp_text)

        result = "PASS" if ok else "FAIL"
        replay_verdicts.append({
            "test_case_id": tc_id,
            "result": result,
            "assertions": assertions,
            "source": "replay",
        })

        orig = orig_verdicts.get(tc_id)
        if orig and orig.get("result") != result:
            diffs.append({
                "test_case_id": tc_id,
                "original_result": orig.get("result"),
                "replay_result": result,
            })

    pass_count = sum(1 for v in replay_verdicts if v["result"] == "PASS")
    fail_count = sum(1 for v in replay_verdicts if v["result"] == "FAIL")
    na_count = sum(1 for v in replay_verdicts if v["result"] == "NOT_APPLICABLE")
    stale_count = sum(1 for v in replay_verdicts if v["result"] == "STALE")

    replay_report = {
        "replay_run_id": replay_id,
        "replay_of_run_id": orig_run_id,
        "replay_dir": str(replay_dir),
        "profile_id": profile.get("id"),
        "suite_version": VERSION,
        "generated_at": generated_at,
        "summary": {
            "PASS": pass_count,
            "FAIL": fail_count,
            "NOT_APPLICABLE": na_count,
            "STALE": stale_count,
            "verdict_diffs": len(diffs),
            "exit_status": 0 if fail_count == 0 else 1,
        },
        "verdict_diffs": diffs,
        "verdicts": replay_verdicts,
    }

    (out / "replay-report.json").write_text(json.dumps(replay_report, indent=2), encoding="utf-8")
    print(f"Replay complete: {pass_count} PASS, {fail_count} FAIL, {len(diffs)} verdict diff(s). Report: {out}/replay-report.json")
    if fail_count > 0:
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="TRQP Conformance Suite runner")
    ap.add_argument("--profile", required=True, help="Path to profile YAML")
    ap.add_argument("--sut", required=True, help="Path to SUT config YAML")
    ap.add_argument("--out", required=True, help="Output directory for evidence artifacts")
    ap.add_argument("--run-id", default=None, help="Optional shared run identifier for Operational Stack workflows")
    ap.add_argument("--target-id", default=None, help="Optional stable target identifier for Operational Stack workflows")
    ap.add_argument("--dry-run", action="store_true",
                    help="Validate inputs and list applicable tests without executing any HTTP requests")
    ap.add_argument("--list-tests", action="store_true",
                    help="Print tests applicable to the selected profile and exit")
    ap.add_argument("--generated-at", default=None,
                    help="Fix the generated_at timestamp for deterministic/reproducible output "
                         "(ISO 8601, e.g. 2026-01-15T00:00:00Z). When omitted, current UTC time is used.")
    ap.add_argument("--fixture-set", default=None,
                    help="Path to a fixture-set JSON file. When provided, canned responses are used "
                         "instead of live HTTP requests, enabling fully deterministic CI runs.")
    ap.add_argument("--replay", default=None,
                    help="Path to a prior run output directory. Re-evaluates assertion logic "
                         "against captured case files without hitting a live SUT. "
                         "Emits replay-report.json in --out with per-assertion diffs.")
    args = ap.parse_args()

    profile = load_yaml(Path(args.profile))
    sut = load_yaml(Path(args.sut))
    out = Path(args.out)

    # Resolve the timestamp to use throughout this run
    generated_at = args.generated_at or now_iso()

    tests = load_yaml(ROOT/"tests/core_tests.yaml")["tests"]
    identifiers = resolve_identifiers(sut)

    if args.list_tests:
        list_tests(tests, profile)
        return

    if args.dry_run:
        print(f"Dry run: profile='{profile.get('id')}', sut base_url='{sut.get('base_url')}'")
        list_tests(tests, profile)
        print("Dry run complete — no HTTP requests were made.")
        return

    # --replay: re-evaluate over a prior run directory
    if args.replay:
        replay_dir = Path(args.replay)
        if not replay_dir.is_dir():
            raise SystemExit(f"--replay path does not exist or is not a directory: {replay_dir}")
        run_replay(replay_dir, out, profile, generated_at)
        return

    # Load fixture set if provided
    fixture_set = None
    fixture_set_sha256 = None
    if args.fixture_set:
        fixture_path = Path(args.fixture_set)
        fixture_set = load_fixture_set(fixture_path)
        fixture_set_sha256 = sha256_file(fixture_path)

    ensure_dirs(out)

    if profile.get("gates", {}).get("require_state_reference") and not sut.get("state_reference"):
        raise SystemExit("Gate failed: sut.state_reference required for this profile.")

    run_id = args.run_id or str(uuid.uuid4())
    base_url = sut["base_url"]
    target_id = args.target_id or sut.get("target_id") or base_url
    run = {
        "test_run_id": run_id,
        "profile_id": profile["id"],
        "out_dir_label": out.name,
        "sut": {k:v for k,v in sut.items() if k != "signing_key_b64"},
        "target_id": target_id,
        "started_at": generated_at,
        "tool": {"name": "trqp-cts", "version": VERSION},
    }

    # Embed fixture set provenance when fixture mode is active
    if fixture_set is not None:
        run["fixture_set"] = {
            "path": args.fixture_set,
            "sha256": fixture_set_sha256,
            "fixture_set_id": fixture_set.get("fixture_set_id"),
        }

    # Embed state reference when declared
    state_ref = sut.get("state_reference")
    if state_ref:
        run["state_reference"] = state_ref

    verdicts = []

    for tc in tests:
        _verdict_override = None
        tc_id = tc["id"]

        applicable_profiles = tc.get("profiles")
        if applicable_profiles and profile.get("id") not in applicable_profiles:
            case = {
                "test_case_id": tc_id,
                "name": tc.get("name"),
                "request": {"method": tc.get("method","POST"), "path": tc["path"], "headers": {}, "body": None},
                "response": {"status": None, "headers": {}, "text": ""},
                "elapsed_ms": 0,
                "assertions": [{"type": "profile_gate", "profiles": applicable_profiles, "profile_id": profile.get("id"), "pass": True}],
                "skipped": True
            }
            case_path = out/"cases"/f"{tc_id}.json"
            case_path.write_text(json.dumps(case, indent=2), encoding="utf-8")
            verdicts.append({"test_case_id": tc_id, "result": "NOT_APPLICABLE", "reason": f"not applicable to profile {profile.get('id')}", "elapsed_ms": 0})
            continue
        try:
            headers = dict(sut.get("default_headers", {}))
            headers.update(tc.get("request", {}).get("headers", {}) or {})
            body = tc.get("request", {}).get("body", None)
            body = apply_identifier_overrides(body, identifiers)

            if profile["id"] == "high_assurance" and tc_id != "TC-SEC-001":
                nonce = "nonce-" + str(uuid.uuid4())
                ts = generated_at
                add_ha_headers(headers, sut, nonce, ts)

            started = time.time()

            # Use fixture set if provided, else make a live HTTP request
            if fixture_set is not None:
                resp = fixture_request(fixture_set, tc_id)
                if resp is None:
                    elapsed_ms = 0
                    case = {
                        "id": tc_id,
                        "name": tc.get("name"),
                        "request": {"method": tc.get("method", "POST"), "path": tc["path"], "headers": headers, "body": body},
                        "response": {"status": None, "headers": {}, "text": ""},
                        "elapsed_ms": 0,
                        "assertions": [{"type": "fixture_missing", "pass": False,
                                        "note": f"No fixture entry for {tc_id} in fixture set"}],
                    }
                    case_path = out/"cases"/f"{tc_id}.json"
                    case_path.write_text(json.dumps(case, indent=2), encoding="utf-8")
                    verdicts.append({"test_case_id": tc_id, "result": "SKIP",
                                     "reason": "no fixture entry", "elapsed_ms": 0})
                    continue
            else:
                resp = http_request(base_url, tc, headers, body)

            elapsed_ms = int((time.time() - started) * 1000)

            case = {
                "id": tc_id,
                "name": tc.get("name"),
                "request": {"method": tc.get("method","POST"), "path": tc["path"], "headers": headers, "body": body},
                "response": {"status": resp.status_code, "headers": dict(resp.headers), "text": resp.text},
                "elapsed_ms": elapsed_ms,
                "assertions": []
            }

            resp_json = None
            exp = tc.get("expect", {})

            needs_json = any(k in exp for k in ["schema","json_path_exists","json_path_equals"]) or exp.get("response_json")
            if needs_json:
                try:
                    resp_json = resp.json()
                    case["response"]["json"] = resp_json
                except Exception:
                    pass

            ok, assertions = _evaluate_assertions(
                tc,
                resp.status_code,
                dict(resp.headers),
                resp_json,
                resp.text,
            )
            case["assertions"] = assertions

            # Special replay test for HA: send the same nonce twice to trigger 409
            if tc_id == "TC-SEC-002" and profile["id"] == "high_assurance" and fixture_set is None:
                resp2 = http_request(base_url, tc, headers, body)
                passed = resp2.status_code == exp.get("status")
                ok &= passed
                case["assertions"].append({"type":"replay","expected":exp.get("status"),"actual":resp2.status_code,"pass":passed})

        except Exception as e:
            elapsed_ms = int((time.time() - started) * 1000) if 'started' in locals() else 0
            case = {
                "id": tc_id,
                "name": tc.get("name"),
                "request": {"method": tc.get("method","POST"), "path": tc.get("path"), "headers": headers if 'headers' in locals() else {}, "body": body if 'body' in locals() else None},
                "response": {"status": None, "headers": {}, "text": ""},
                "elapsed_ms": elapsed_ms,
                "assertions": [{"type": "exception", "pass": False, "error": str(e)}],
            }
            ok = False
            _verdict_override = "ERROR"
        case_path = out/"cases"/f"{tc_id}.json"
        case_path.write_text(json.dumps(case, indent=2), encoding="utf-8")
        verdicts.append({"test_case_id": tc_id, "result": (_verdict_override if _verdict_override else ("PASS" if ok else "FAIL")), "elapsed_ms": elapsed_ms})

    run["ended_at"] = generated_at
    (out/"run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    (out/"verdicts.json").write_text(json.dumps(verdicts, indent=2), encoding="utf-8")

    pass_count = sum(1 for v in verdicts if v["result"] == "PASS")
    fail_count = sum(1 for v in verdicts if v["result"] == "FAIL")
    skip_count = sum(1 for v in verdicts if v["result"] == "SKIP")
    na_count = sum(1 for v in verdicts if v["result"] == "NOT_APPLICABLE")
    error_count = sum(1 for v in verdicts if v["result"] == "ERROR")
    xfail_count = sum(1 for v in verdicts if v["result"] == "XFAIL")
    applicable = len(verdicts) - na_count
    evaluated = pass_count + fail_count + error_count + xfail_count
    coverage_index = round((evaluated / applicable) * 100.0, 2) if applicable else 100.0
    evidence_completeness = round(((pass_count + skip_count) / applicable) * 100.0, 2) if applicable else 100.0
    summary_counts = {
        "PASS": pass_count,
        "FAIL": fail_count,
        "SKIP": skip_count,
        "NOT_APPLICABLE": na_count,
        "ERROR": error_count,
        "XFAIL": xfail_count,
        "coverage_index": coverage_index,
        "evidence_completeness": evidence_completeness,
        "exit_status": 0 if all(v["result"] in ["PASS", "NOT_APPLICABLE"] for v in verdicts) else 1,
    }
    cts_report = {
        "run_id": run_id,
        "target_id": target_id,
        "generated_at": generated_at,
        "profile": profile["id"],
        "profile_id": profile["id"],
        "suite_version": VERSION,
        "tool": {"name": "trqp-cts", "version": VERSION},
        "summary": summary_counts,
        "results": verdicts,
    }
    (out/"cts-report.json").write_text(json.dumps(cts_report, indent=2), encoding="utf-8")

    manifest = {"generated_at": generated_at, "hashes": {}}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name not in ["bundle.zip","manifest.sig"]:
            manifest["hashes"][str(p.relative_to(out))] = sha256_file(p)

    manifest_path = out/"manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if profile.get("evidence", {}).get("sign_manifest"):
        key_b64 = sut.get("signing_key_b64")
        if not key_b64:
            raise SystemExit("sign_manifest enabled but sut.signing_key_b64 missing")
        sk = SigningKey(key_b64.encode("utf-8"), encoder=Base64Encoder)
        sig = sk.sign(manifest_path.read_bytes()).signature
        (out/"manifest.sig").write_bytes(sig)

    if profile.get("evidence", {}).get("bundle", True):
        bundle = out/"bundle.zip"
        with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for p in sorted(out.rglob("*")):
                if p.is_file() and p.name != "bundle.zip":
                    z.write(p, arcname=str(p.relative_to(out)))

    descriptor = {
        "bundle_version": "0.1.0",
        "run": run,
        "artifacts": {
            "run_json": "run.json",
            "verdicts": "verdicts.json",
            "manifest": "manifest.json",
            "cases_dir": "cases"
        }
    }
    if (out/"manifest.sig").exists():
        descriptor["artifacts"]["signature"] = "manifest.sig"

    artifact_index = []

    ARTIFACT_KIND_MAP = {
        "cts_run_json": "conformance_run_metadata",
        "cts_verdicts": "conformance_verdicts",
        "cts_manifest": "conformance_manifest",
        "cts_manifest_sig": "conformance_manifest_signature",
        "cts_case_file": "conformance_case_artifact",
        "cts_bundle_zip": "conformance_evidence_bundle_zip",
        "cts_bundle_descriptor": "conformance_evidence_bundle_descriptor",
        "cts_checksums": "evidence_bundle_checksums",
        "cts_report": "conformance_report",
    }

    def add_idx(kind: str, rel_path: str, notes: str | None = None):
        p = out/rel_path
        entry = {
            "kind": kind,
            "artifact_kind": ARTIFACT_KIND_MAP.get(kind),
            "path": rel_path,
            "produced_by": "trqp-cts",
        }
        if p.exists() and p.is_file():
            entry["sha256"] = sha256_file(p)
            mt = guess_media_type(p)
            if mt:
                entry["media_type"] = mt
        if notes:
            entry["notes"] = notes
        artifact_index.append(entry)

    add_idx("cts_run_json", "run.json")
    add_idx("cts_report", "cts-report.json", notes="Operational Stack conformance report.")
    add_idx("cts_verdicts", "verdicts.json")
    add_idx("cts_manifest", "manifest.json")
    if (out/"manifest.sig").exists():
        add_idx("cts_manifest_sig", "manifest.sig", notes="Signature over manifest.json (high-assurance profiles).")

    cases_dir = out/"cases"
    if cases_dir.exists():
        for p in sorted(cases_dir.glob("*.json")):
            add_idx("cts_case_file", str(p.relative_to(out)))

    if (out/"bundle.zip").exists():
        descriptor["artifacts"]["bundle_zip"] = "bundle.zip"
        add_idx("cts_bundle_zip", "bundle.zip")

    descriptor["artifact_index"] = artifact_index
    (out/"bundle_descriptor.json").write_text(json.dumps(descriptor, indent=2), encoding="utf-8")
    add_idx("cts_bundle_descriptor", "bundle_descriptor.json")

    checksums = []
    for a in artifact_index:
        if a.get("sha256") and a.get("path"):
            checksums.append({"path": a["path"], "sha256": a["sha256"]})
    checksums_obj = {
        "checksums_version": "0.1.0",
        "algorithm": "sha256",
        "generated_by": "trqp-cts",
        "generated_at": generated_at,
        "entries": sorted(checksums, key=lambda e: e["path"]),
    }
    (out/"checksums.json").write_text(json.dumps(checksums_obj, indent=2), encoding="utf-8")
    add_idx("cts_checksums", "checksums.json")

    print(f"OK: evidence written to {out}")

if __name__ == "__main__":
    main()
