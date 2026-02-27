"""Proof-of-concept TRQP service used by the Conformance Suite examples.

This file is intentionally simple, but it is also the most likely copy/paste starting point.
Key expectations:
- Keep responses deterministic for tests.
- Make security-sensitive decisions explicit in code (authn/z, logging, rate limiting).
- Do not treat this as production-ready without hardening and threat review.
"""

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional, Dict
import time

app = FastAPI(title="TRQP PoC SUT", version="0.1.0")

NONCES: Dict[str, float] = {}
MAX_SKEW_SECONDS = 120

def is_ha(req: Request) -> bool:
    return req.headers.get("X-Auth-Mode", "").lower() == "high_assurance"

def require_auth(req: Request):
    if not is_ha(req):
        return
    if req.headers.get("X-API-Key") != "demo-secret":
        raise HTTPException(status_code=401, detail={"error":"unauthorized","message":"Missing/invalid API key","code":"UNAUTHORIZED"})
    nonce = req.headers.get("X-Nonce")
    ts = req.headers.get("X-Timestamp")
    if not nonce or not ts:
        raise HTTPException(status_code=401, detail={"error":"unauthorized","message":"Missing nonce/timestamp","code":"MISSING_NONCE_TS"})
    if nonce in NONCES:
        raise HTTPException(status_code=409, detail={"error":"replay_detected","message":"Nonce already used","code":"REPLAY"})
    NONCES[nonce] = time.time()
    try:
        t = datetime.fromisoformat(ts.replace("Z","+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail={"error":"bad_request","message":"Invalid timestamp format","code":"BAD_TS"})
    skew = abs((datetime.now(timezone.utc) - t).total_seconds())
    if skew > MAX_SKEW_SECONDS:
        raise HTTPException(status_code=400, detail={"error":"bad_request","message":"Timestamp skew too large","code":"SKEW"})

def echo_corr(req: Request, headers: Dict[str,str]):
    cid = req.headers.get("X-Correlation-Id")
    if cid:
        headers["X-Correlation-Id"] = cid

class Context(BaseModel):
    timestamp: Optional[str] = None

class AuthorizationQuery(BaseModel):
    authority_id: str
    entity_id: str
    action: str
    resource: Optional[str] = None
    context: Optional[Context] = None

class RecognitionQuery(BaseModel):
    authority_id: str
    subject_authority_id: str
    context: Optional[Context] = None

@app.post("/authorization")
async def authorization(q: AuthorizationQuery, request: Request):
    require_auth(request)
    headers = {"Content-Type":"application/json; charset=utf-8"}
    echo_corr(request, headers)

    authorized = (q.entity_id == "did:example:logistics-sp-123" and q.action == "issue-transport-credential")
    resp = {
        "authority_id": q.authority_id,
        "entity_id": q.entity_id,
        "action": q.action,
        "resource": q.resource,
        "decision": {
            "authorized": authorized,
            "reason": "Authorization found and currently valid." if authorized else "No matching authorization record found.",
            "valid_from": "2024-01-01T00:00:00Z",
            "valid_until": "2026-01-01T00:00:00Z",
            "assertion_reference": "urn:vc:statuslist:123#entry-99" if authorized else None
        }
    }
    from fastapi.responses import JSONResponse
    return JSONResponse(content=resp, headers=headers)

@app.post("/recognition")
async def recognition(q: RecognitionQuery, request: Request):
    require_auth(request)
    headers = {"Content-Type":"application/json; charset=utf-8"}
    echo_corr(request, headers)

    recognised = (q.subject_authority_id == "did:example:foreign-authority-xyz")
    resp = {
        "authority_id": q.authority_id,
        "subject_authority_id": q.subject_authority_id,
        "statement": {
            "recognised": recognised,
            "reason": "Recognised according to current governance framework." if recognised else "No recognition relationship found.",
            "recognised_since": "2024-06-01T00:00:00Z" if recognised else None,
            "valid_until": None,
            "governance_reference": "https://example.org/gf/transport-recognition-v1" if recognised else None
        }
    }
    from fastapi.responses import JSONResponse
    return JSONResponse(content=resp, headers=headers)

@app.get("/.well-known/trust-registries")
async def discovery():
    return [{
        "authority_id": "did:example:transport-ministry",
        "trqp_endpoint": "http://127.0.0.1:8000",
        "governance_reference": "https://example.org/gf/transport-v1",
        "profiles": ["baseline","enterprise","high_assurance"]
    }]
