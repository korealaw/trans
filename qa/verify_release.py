"""Release gate: exact tested app bytes, data consistency and syntax. No dependencies."""
from pathlib import Path
import collections,csv,hashlib,json,re,subprocess,sys,tempfile
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
HASHES={'01_PHONE.html':'af6231bd4634b23fa03414631b5c4d7fbeff1cbe','02_PERSONAL_PC.html':'45c4e3c64677bc4cf730104188d734c4ae64e5ce','03_INTRANET_PC.html':'006475fdb8406afb7a9e9ae4510cea9f060e4f38'}
rows=list(csv.DictReader((ROOT/'question_db/MG_MASTER_QUESTION_DB_300.csv').open(encoding='utf-8-sig')))
reserve=list(csv.DictReader((ROOT/'question_db/MG_RESERVE_40.csv').open(encoding='utf-8-sig')))
master={r['id']:r for r in rows};assert len(rows)==len(master)==300
assert len(reserve)==40 and set(r['id'] for r in reserve)==set(r['id'] for r in rows if r['learning_pool']=='RESERVE')
reports=[];common=None
for filename,wanted in HASHES.items():
    raw=(ROOT/filename).read_bytes();sha=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert sha==wanted,('Not tested app bytes',filename,sha)
    text=raw.decode('utf-8');js=re.search(r'<script>(.*?)</script>',text,re.S)[1]
    with tempfile.NamedTemporaryFile(mode='w',suffix='.js',encoding='utf-8') as t:t.write(js);t.flush();subprocess.run(['node','--check',t.name],check=True)
    fn=re.findall(r'^function ([$\w]+)\(',js,re.M);assert len(fn)==len(set(fn))
    data={k:json.loads(re.search(r'^const '+k+r'=(.*);$',js,re.M)[1]) for k in ['CONCEPTS','DAILIES','QUESTIONS','QUICK_IDS','MOCK']}
    if common is not None:assert data==common
    common=data;qmap={q['id']:q for q in data['QUESTIONS']};quick=set(data['QUICK_IDS']);focus=set(qmap)-quick
    assert len(qmap)==len(data['QUESTIONS'])==260 and len(quick)==52 and len(focus)==208
    assert {q['id'] for q in data['MOCK']}<=focus and len(data['MOCK'])==20 and len({q['concept'] for q in data['MOCK']})==20
    concepts={c['id'] for c in data['CONCEPTS']};assert len(concepts)==58 and len(data['DAILIES'])==5
    daily_ids=[id for d in data['DAILIES'] for id in d['questions']];assert len(daily_ids)==260 and set(daily_ids)==set(qmap)
    for q in qmap.values():
        r=master[q['id']];assert len(q['options'])==len(q['optionReasons'])==4 and len(set(q['options']))==4
        assert q['concept'] in concepts and 0<=q['answer']<=3 and q['answer']==int(r['answer'])-1
        for key,col in {'question':'question','step1':'step1_core','step2':'step2_detail','trap':'step3_trap','concept':'concept_id','daily':'active_daily_id','memoryHook':'memory_hook'}.items():assert q.get(key,'')==r.get(col,''),(q['id'],key)
        for i in range(4):assert q['options'][i]==r['option'+str(i+1)] and q['optionReasons'][i]==r['option_reason'+str(i+1)]
        assert q['sources'] and q['sourceRefs'] and r['learning_pool']==('QUICK' if q['id'] in quick else 'FOCUS')
    assert 'mg_saemaeul_learning_rc2_progress_v1' in js and 'constFLOW_SCHEMA_VERSION=23' in js.replace(' ','')
    assert not re.search(r'(?:src|href)\s*=\s*["\']https?://',text,re.I)
    assert not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(',js)
    reports.append({'file':filename,'git_blob_sha':sha,'bytes':len(raw),'syntax':'PASS','duplicate_functions':0,'active_csv_match':260,'external_runtime_network_calls':0})
counts=collections.Counter(q['concept'] for q in common['QUESTIONS']);qc={q['concept'] for q in common['QUESTIONS'] if q['id'] in quick}
report={'result':'PASS','files':reports,'active':260,'quick':52,'focus':208,'master_including_reserve':300,'reserve_subset':40,'concepts':58,'single_question_concepts':[c['id'] for c in common['CONCEPTS'] if counts[c['id']]==1],'focus_only_concepts':[c['id'] for c in common['CONCEPTS'] if c['id'] not in qc],'focus_daily_counts':{d['id']:len(set(d['questions'])&focus) for d in common['DAILIES']},'answer_distribution_master':dict(collections.Counter(r['answer'] for r in rows)),'legal_currency':'NOT_REVALIDATED; data alignment is not substantive legal validation'}
(ROOT/'qa').mkdir(exist_ok=True);(ROOT/'qa/static_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
