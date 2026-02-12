import argparse, json, time, hashlib, zipfile, uuid
from pathlib import Path
from datetime import datetime, timezone
import yaml
import requests
from jsonschema import validate as js_validate
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder

ROOT = Path(__file__).resolve().parent.parent

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())

def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def json_path_get(doc, path: str):
    if not path.startswith("$."):
        raise ValueError("Only supports paths starting with $.")
    cur = doc
    toks = path[2:].split(".")
    for t in toks:
        if "[" in t and t.endswith("]"):
            key, idx = t[:-1].split("[", 1)
            cur = cur.get(key)
            cur = cur[int(idx)]
        else:
            cur = cur.get(t) if isinstance(cur, dict) else None
    return cur

def ensure_dirs(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    (out/"cases").mkdir(exist_ok=True)

def http_request(base_url: str, tc: dict, headers: dict, body):
    url = base_url.rstrip("/") + tc["path"]
    method = tc.get("method", "POST").upper()
    return requests.request(method, url, headers=headers, json=body, timeout=20)

def add_ha_headers(headers: dict, sut: dict, nonce: str, ts: str):
    # Demo HA control plane (example SUT expects these)
    headers["X-Auth-Mode"] = "high_assurance"
    headers["X-API-Key"] = sut.get("api_key", "demo-secret")
    headers["X-Nonce"] = nonce
    headers["X-Timestamp"] = ts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--sut", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    profile = load_yaml(Path(args.profile))
    sut = load_yaml(Path(args.sut))
    out = Path(args.out)

    ensure_dirs(out)

    if profile.get("gates", {}).get("require_state_reference") and not sut.get("state_reference"):
        raise SystemExit("Gate failed: sut.state_reference required for this profile.")

    tests = load_yaml(ROOT/"tests/core_tests.yaml")["tests"]

    run_id = out.name or str(uuid.uuid4())
    run = {
        "test_run_id": run_id,
        "profile_id": profile["id"],
        "sut": {k:v for k,v in sut.items() if k != "signing_key_b64"},
        "started_at": now_iso(),
        "tool": {"name": "trqp-cts", "version": "0.1.0"},
    }

    base_url = sut["base_url"]
    verdicts = []

    for tc in tests:
        tc_id = tc["id"]
        headers = dict(sut.get("default_headers", {}))
        headers.update(tc.get("request", {}).get("headers", {}) or {})
        body = tc.get("request", {}).get("body", None)

        # If profile is HA, add HA headers for tests except TC-SEC-001 (which asserts unauth)
        if profile["id"] == "high_assurance" and tc_id != "TC-SEC-001":
            nonce = "nonce-" + str(uuid.uuid4())
            ts = now_iso()
            add_ha_headers(headers, sut, nonce, ts)

        started = time.time()
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

        ok = True
        exp = tc.get("expect", {})

        if "status" in exp:
            passed = resp.status_code == exp["status"]
            ok &= passed
            case["assertions"].append({"type":"status", "expected":exp["status"], "actual":resp.status_code, "pass":passed})

        if "status_in" in exp:
            passed = resp.status_code in exp["status_in"]
            ok &= passed
            case["assertions"].append({"type":"status_in", "expected":exp["status_in"], "actual":resp.status_code, "pass":passed})

        resp_json = None
        needs_json = any(k in exp for k in ["schema","json_path_exists","json_path_equals"]) or exp.get("response_json")
        if needs_json:
            try:
                resp_json = resp.json()
                case["response"]["json"] = resp_json
                case["assertions"].append({"type":"json_parse","pass":True})
            except Exception:
                ok = False
                case["assertions"].append({"type":"json_parse","pass":False})

        if "response_header_contains" in exp:
            for k,v in exp["response_header_contains"].items():
                actual = resp.headers.get(k)
                passed = (actual is not None and v in actual) if k.lower()=="content-type" else (actual == v)
                ok &= passed
                case["assertions"].append({"type":"header_contains","header":k,"expected":v,"actual":actual,"pass":passed})

        if exp.get("schema") and resp_json is not None:
            schema = load_json(ROOT/exp["schema"])
            try:
                js_validate(instance=resp_json, schema=schema)
                case["assertions"].append({"type":"schema","schema":exp["schema"],"pass":True})
            except Exception as e:
                ok = False
                case["assertions"].append({"type":"schema","schema":exp["schema"],"pass":False,"error":str(e)})

        if exp.get("json_path_exists") and resp_json is not None:
            for p in exp["json_path_exists"]:
                passed = json_path_get(resp_json, p) is not None
                ok &= passed
                case["assertions"].append({"type":"json_path_exists","path":p,"pass":passed})

        if exp.get("json_path_equals") and resp_json is not None:
            for p, expected in exp["json_path_equals"]:
                actual = json_path_get(resp_json, p)
                passed = (actual == expected)
                ok &= passed
                case["assertions"].append({"type":"json_path_equals","path":p,"expected":expected,"actual":actual,"pass":passed})

        # Special replay test for HA: send the same nonce twice to trigger 409
        if tc_id == "TC-SEC-002" and profile["id"] == "high_assurance":
            # Reuse the same nonce/timestamp headers
            resp2 = http_request(base_url, tc, headers, body)
            passed = resp2.status_code == exp["status"]
            ok &= passed
            case["assertions"].append({"type":"replay","expected":exp["status"],"actual":resp2.status_code,"pass":passed})

        case_path = out/"cases"/f"{tc_id}.json"
        case_path.write_text(json.dumps(case, indent=2), encoding="utf-8")

        verdicts.append({"test_case_id": tc_id, "result": "PASS" if ok else "FAIL", "elapsed_ms": elapsed_ms})

    run["ended_at"] = now_iso()
    (out/"run.json").write_text(json.dumps(run, indent=2), encoding="utf-8")
    (out/"verdicts.json").write_text(json.dumps(verdicts, indent=2), encoding="utf-8")

    manifest = {"generated_at": now_iso(), "hashes": {}}
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

    print(f"OK: evidence written to {out}")

if __name__ == "__main__":
    main()
