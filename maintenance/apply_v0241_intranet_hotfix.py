from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
FILES=['01_PHONE.html','02_PERSONAL_PC.html','03_INTRANET_PC.html']
BASE={'01_PHONE.html':'af6231bd4634b23fa03414631b5c4d7fbeff1cbe','02_PERSONAL_PC.html':'45c4e3c64677bc4cf730104188d734c4ae64e5ce','03_INTRANET_PC.html':'006475fdb8406afb7a9e9ae4510cea9f060e4f38'}
WANT={'01_PHONE.html':'de28e913e9f76daa1723784899e8a5fa6d6104e2','02_PERSONAL_PC.html':'0d5c73cf2c15f0a646bff2c662cd09134c24a2b8','03_INTRANET_PC.html':'9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b'}
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
for name in FILES:
 p=ROOT/name; raw=p.read_bytes(); got=blob(raw)
 if got==WANT[name]:continue
 if got!=BASE[name]:raise SystemExit(f'Unexpected baseline {name}: {got}')
 s=raw.decode('utf-8').replace('RC4 v0.24','RC4 v0.24.1')
 if name=='03_INTRANET_PC.html':
  s=s.replace('RC4 v0.24.1.1 - INTRANET','RC4 v0.24.1 - INTRANET')
  old='body{padding:14px;background:#b2b2b2}'
  if old not in s:raise SystemExit('desktop host background baseline missing')
  s=s.replace(old,'body{padding:14px;background:#8fb9d5}',1)
  marker='#app{filter:grayscale(1)}'
  if marker not in s:raise SystemExit('global grayscale baseline missing')
  s=s.replace(marker,'',1)
 p.write_text(s,encoding='utf-8')
 if blob(p.read_bytes())!=WANT[name]:raise SystemExit(f'Output hash mismatch {name}: {blob(p.read_bytes())}')
print('RC4 v0.24.1 hotfix generated with exact tested hashes')
