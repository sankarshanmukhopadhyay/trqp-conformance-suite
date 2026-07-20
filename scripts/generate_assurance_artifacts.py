#!/usr/bin/env python3
from pathlib import Path
import json, yaml, hashlib, subprocess, sys, shutil
root=Path(__file__).resolve().parents[1]
out=root/'artifacts'; val=out/'validation'; tr=out/'traceability'
shutil.rmtree(val,ignore_errors=True); val.mkdir(parents=True); tr.mkdir(parents=True,exist_ok=True)
run='cts-local-assurance'; target='trqp-reference-fixture'
cmd=[sys.executable,'cts/run.py','--profile','profiles/baseline.yaml','--sut','examples/sut.local.yaml.example','--out',str(val/'run'),'--fixture-set','fixtures/baseline.fixture-set.json','--run-id',run,'--target-id',target,'--generated-at','2026-07-20T00:00:00Z']
subprocess.run(cmd,cwd=root,check=True)
reports=list((val/'run').glob('*.json'))
report=next((p for p in reports if 'report' in p.name), reports[0] if reports else None)
if report is None: raise SystemExit('CTS produced no JSON report')
shutil.copy2(report,val/'cts-report.json')
req=yaml.safe_load((root/'requirements/core.yaml').read_text())
tests=yaml.safe_load((root/'tests/core_tests.yaml').read_text())
def items(x):
  if isinstance(x,list): return x
  if isinstance(x,dict):
    for k in ('requirements','tests','items'):
      if isinstance(x.get(k),list): return x[k]
  return []
rs=items(req); ts=items(tests)
ids=lambda seq:[str(i.get('id') or i.get('requirement_id') or i.get('test_id')) for i in seq if isinstance(i,dict)]
coverage={'schema_version':'1.0','producer':'trqp-conformance-suite','version':(root/'VERSION').read_text().strip(),'requirements':ids(rs),'tests':ids(ts),'requirement_count':len(rs),'test_count':len(ts),'evidence':'artifacts/validation/cts-report.json'}
(tr/'cts-requirement-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
neg=[x for x in ts if isinstance(x,dict) and any(w in json.dumps(x).lower() for w in ('negative','invalid','reject','error','missing','expired'))]
(tr/'negative-test-coverage.json').write_text(json.dumps({'schema_version':'1.0','producer':'trqp-conformance-suite','negative_test_count':len(neg),'test_ids':ids(neg)},indent=2)+'\n')
idx=[]
for p in sorted(out.rglob('*')):
  if p.is_file(): idx.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(val/'evidence-index.json').write_text(json.dumps({'run_id':run,'target_id':target,'artifacts':idx},indent=2)+'\n')
print('CTS assurance artifacts generated')
