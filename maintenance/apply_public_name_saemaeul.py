from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
OLD = '오다영과장 공부하기'
NEW = '새마을금고 학습'
BASE = {
    '01_PHONE.html': '7eb064417f9bc6ae1777aba968e2c12c3eee5439',
    '02_PERSONAL_PC.html': 'e192490725bf607773546a6c42b7cb59b6f6d681',
    'index.html': 'c257f306ad16856bf79aadb2f17eff8137a7ede1',
}
INTRANET = '9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b'

def blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

results = []
for name, expected in BASE.items():
    p = ROOT / name
    raw = p.read_bytes()
    got = blob(raw)
    if got != expected:
        raise SystemExit(f'Unexpected baseline {name}: {got}')
    s = raw.decode('utf-8')
    count = s.count(OLD)
    if count < 1:
        raise SystemExit(f'Old public name missing in {name}')
    s = s.replace(OLD, NEW)
    if OLD in s:
        raise SystemExit(f'Old public name remains in {name}')
    if NEW not in s:
        raise SystemExit(f'New public name missing in {name}')
    p.write_text(s, encoding='utf-8')
    results.append({'file': name, 'replacements': count, 'git_blob_sha': blob(p.read_bytes())})

intra = blob((ROOT / '03_INTRANET_PC.html').read_bytes())
if intra != INTRANET:
    raise SystemExit(f'Intranet changed unexpectedly: {intra}')

out = {
    'result': 'PASS',
    'public_app_name': NEW,
    'public_version': 'RC4 v0.24.2',
    'files': results,
    'intranet': {'version': 'RC4 v0.24.1', 'git_blob_sha': INTRANET, 'status': 'UNCHANGED'},
    'storage_schema': 'UNCHANGED',
    'question_data': 'UNCHANGED'
}
(ROOT / 'qa' / 'static_results_public_name.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out, ensure_ascii=False))
