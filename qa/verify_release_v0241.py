from pathlib import Path
import collections,csv,hashlib,json,re,subprocess,sys,tempfile,base64
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
HASHES={'01_PHONE.html':'de28e913e9f76daa1723784899e8a5fa6d6104e2','02_PERSONAL_PC.html':'0d5c73cf2c15f0a646bff2c662cd09134c24a2b8','03_INTRANET_PC.html':'9042cffb25e5d84de29c1cbf0f86cd3c29a15b7b'}
LEGACY_BG_SHA256='3bea84654e733a6b45a887e139cd8f528eff90e11b1d237bb8897dfaf020e097'
rows=list(csv.DictReader((ROOT/'question_db/MG_MASTER_QUESTION_DB_300.csv').open(encoding='utf-8-sig')))
reserve=list(csv.DictReader((ROOT/'question_db/MG_RESERVE_40.csv').open(encoding='utf-8-sig')))
master={r['id']:r for r in rows};assert len(rows)==len(master)==300
assert len(reserve)==40 and set(r['id'] for r in reserve)==set(r['id'] for r in rows if r['learning_pool']=='RESERVE')
reports=[];common=None
for filename,wanted in HASHES.items():
 raw=(ROOT/filename).read_bytes();sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert sha==wanted,(filename,sha)
 text=raw.decode('utf-8');js=re.search(r'<script>(.*?)</script>',text,re.S)[1]
 with tempfile.NamedTemporaryFile(mode='w',suffix='.js',encoding='utf-8') as t:
  t.write(js);t.flush();subprocess.run(['node','--check',t.name],check=True)
 fn=re.findall(r'^function ([$\w]+)\(',js,re.M);assert len(fn)==len(set(fn))
 data={k:json.loads(re.search(r'^const '+k+r'=(.*);$',js,re.M)[1]) for k in ['CONCEPTS','DAILIES','QUESTIONS','QUICK_IDS','MOCK']}
 if common is not None:assert data==common
 common=data;qmap={q['id']:q for q in data['QUESTIONS']};quick=set(data['QUICK_IDS']);focus=set(qmap)-quick
 assert len(qmap)==260 and len(quick)==52 and len(focus)==208 and len(data['MOCK'])==20 and len(data['CONCEPTS'])==58 and len(data['DAILIES'])==5
 assert {q['id'] for q in data['MOCK']}<=focus and len({q['concept'] for q in data['MOCK']})==20
 daily_ids=[id for d in data['DAILIES'] for id in d['questions']];assert len(daily_ids)==260 and set(daily_ids)==set(qmap)
 concepts={c['id'] for c in data['CONCEPTS']}
 for q in qmap.values():
  r=master[q['id']];assert len(q['options'])==len(q['optionReasons'])==4 and len(set(q['options']))==4
  assert q['concept'] in concepts and q['answer']==int(r['answer'])-1
  for key,col in {'question':'question','step1':'step1_core','step2':'step2_detail','trap':'step3_trap','concept':'concept_id','daily':'active_daily_id','memoryHook':'memory_hook'}.items():assert q.get(key,'')==r.get(col,'')
  for i in range(4):assert q['options'][i]==r['option'+str(i+1)] and q['optionReasons'][i]==r['option_reason'+str(i+1)]
 assert 'mg_saemaeul_learning_rc2_progress_v1' in js and 'constFLOW_SCHEMA_VERSION=23' in js.replace(' ','')
 assert not re.search(r'(?:src|href)\s*=\s*["\']https?://',text,re.I) and not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(',js)
 reports.append({'file':filename,'git_blob_sha':sha,'bytes':len(raw),'syntax':'PASS','duplicate_functions':0,'active_csv_match':260,'external_runtime_network_calls':0})
intra=(ROOT/'03_INTRANET_PC.html').read_text(encoding='utf-8')
m=re.search(r'background:url\(data:image/png;base64,([^\)]+)\)',intra);assert m
bgsha=hashlib.sha256(base64.b64decode(m.group(1))).hexdigest();assert bgsha==LEGACY_BG_SHA256
assert '#app{filter:grayscale(1)}' not in intra
assert 'body{padding:14px;background:#8fb9d5}' in intra
assert '.main{font-size:12px!important;color:#333!important;background:#f4f4f4!important}' in intra
counts=collections.Counter(q['concept'] for q in common['QUESTIONS']);qc={q['concept'] for q in common['QUESTIONS'] if q['id'] in set(common['QUICK_IDS'])}
report={'result':'PASS','version':'RC4 v0.24.1','files':reports,'active':260,'quick':52,'focus':208,'master_including_reserve':300,'reserve_subset':40,'concepts':58,'single_question_concepts':[c['id'] for c in common['CONCEPTS'] if counts[c['id']]==1],'focus_only_concepts':[c['id'] for c in common['CONCEPTS'] if c['id'] not in qc],'intranet_color_boundary':{'legacy_background_sha256':bgsha,'global_grayscale_filter':'ABSENT','execution_panel':'NEUTRAL_GRAYSCALE_CSS'},'legal_currency':'NOT_REVALIDATED; data alignment is not substantive legal validation'}
(ROOT/'qa/static_results_v0241.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
