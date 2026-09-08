from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
FILES=['01_PHONE.html','02_PERSONAL_PC.html']
BASE={'01_PHONE.html':'de28e913e9f76daa1723784899e8a5fa6d6104e2','02_PERSONAL_PC.html':'0d5c73cf2c15f0a646bff2c662cd09134c24a2b8'}
WANT={'01_PHONE.html':'7eb064417f9bc6ae1777aba968e2c12c3eee5439','02_PERSONAL_PC.html':'e192490725bf607773546a6c42b7cb59b6f6d681'}
INTRANET='9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b'
NEW='오다영과장 공부하기'
CSS='''\n/* RC4 v0.24.2 - public app brand hierarchy */\n.app-main-title{margin:0 0 16px;font-size:32px;line-height:1.18;letter-spacing:-1px;font-weight:950;color:var(--rc-ink);word-break:keep-all}\n@media(max-width:390px){.app-main-title{font-size:28px;margin-bottom:13px}}\n@media(min-width:900px){.app-main-title{font-size:34px;margin-bottom:18px}}\n'''
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
for name in FILES:
 p=ROOT/name;raw=p.read_bytes();got=blob(raw)
 if got==WANT[name]:continue
 if got!=BASE[name]:raise SystemExit(f'Unexpected baseline {name}: {got}')
 s=raw.decode('utf-8')
 if s.count('새마을금고 학습')!=6:raise SystemExit(f'Unexpected brand count {name}')
 s=s.replace('새마을금고 학습',NEW).replace('RC4 v0.24.1','RC4 v0.24.2')
 marker='/* RC4 v0.24.2 - mandatory 5-minute gate -> 20+ focus sequence */'
 if marker not in s:raise SystemExit(f'CSS marker missing {name}')
 s=s.replace(marker,CSS+'\n'+marker,1)
 old=f"return shell(`${{chrome('{NEW}')}}<div class=\"rc4-home\"><div class=\"rc4-intro\">"
 new=f"return shell(`${{chrome('{NEW}')}}<div class=\"rc4-home\"><h1 class=\"app-main-title\">{NEW}</h1><div class=\"rc4-intro\">"
 if old not in s:raise SystemExit(f'Home marker missing {name}')
 s=s.replace(old,new,1)
 p.write_text(s,encoding='utf-8')
 if blob(p.read_bytes())!=WANT[name]:raise SystemExit(f'Output hash mismatch {name}: {blob(p.read_bytes())}')
intra=blob((ROOT/'03_INTRANET_PC.html').read_bytes())
if intra!=INTRANET:raise SystemExit(f'Intranet changed unexpectedly: {intra}')
result={'result':'PASS','version':'RC4 v0.24.2','public_app_name':NEW,'public_files':[{ 'file':n,'git_blob_sha':WANT[n]} for n in FILES],'intranet':{'git_blob_sha':INTRANET,'status':'UNCHANGED_RC4_V0241'}}
(ROOT/'qa'/'static_results_v0242.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('RC4 v0.24.2 public branding generated with exact tested hashes')
