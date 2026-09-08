from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
NAME = '새마을금고 학습'
DESC = '새마을금고 학습 웹앱 · 5분 문제와 집중학습으로 이어지는 문제 중심 학습'
BASE = {
    'index.html': 'f1a82149e587caafc82f8d06e3b1af2c6fc0636e',
    '01_PHONE.html': '06821f05ee482bf5b653eef3c5e0bddc45130f92',
    '02_PERSONAL_PC.html': '7fc131d8a29dffd35959489e0c783e08595443e1',
}
URLS = {
    'index.html': 'https://korealaw.github.io/trans/',
    '01_PHONE.html': 'https://korealaw.github.io/trans/01_PHONE.html',
    '02_PERSONAL_PC.html': 'https://korealaw.github.io/trans/02_PERSONAL_PC.html',
}
INTRANET = '9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b'

def blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

results=[]
for name, expected in BASE.items():
    p=ROOT/name
    raw=p.read_bytes(); got=blob(raw)
    if got != expected:
        raise SystemExit(f'Unexpected baseline {name}: {got}')
    s=raw.decode('utf-8')
    if '오다영과장 공부하기' in s:
        raise SystemExit(f'Old public name remains in {name}')
    marker='</title>'
    if marker not in s:
        raise SystemExit(f'title marker missing in {name}')
    url=URLS[name]
    meta=(f'\n<meta name="description" content="{DESC}">'
          f'\n<meta property="og:type" content="website">'
          f'\n<meta property="og:site_name" content="{NAME}">'
          f'\n<meta property="og:title" content="{NAME}">'
          f'\n<meta property="og:description" content="{DESC}">'
          f'\n<meta property="og:url" content="{url}">')
    if 'property="og:title"' in s:
        raise SystemExit(f'OG metadata already exists in {name}')
    s=s.replace(marker, marker+meta, 1)
    p.write_text(s, encoding='utf-8')
    results.append({'file':name,'git_blob_sha':blob(p.read_bytes()),'og_url':url})

intra=blob((ROOT/'03_INTRANET_PC.html').read_bytes())
if intra != INTRANET:
    raise SystemExit(f'Intranet changed unexpectedly: {intra}')

out={'result':'PASS','public_app_name':NAME,'kakao_og':'EXPLICIT','files':results,'intranet':{'git_blob_sha':INTRANET,'status':'UNCHANGED'}}
(ROOT/'qa'/'static_results_kakao_og.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
