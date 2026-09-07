"""Hash-guarded deterministic update. Generates standalone HTML; no remote code.
Usage: python maintenance/apply_v024.py [--source DIR] [--dest DIR]
All three inputs and outputs are checked before any app file is replaced.
"""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,tempfile
EXPECTED={'01_PHONE.html':'1144c5fea5b126d54d1940d3a1ff25574949018b','02_PERSONAL_PC.html':'0ca233283df759831ddac0a17dd3bc2e311291c1','03_INTRANET_PC.html':'621e54e9f62b6f02701934e2a902b65a01bf4807'}
def blob_sha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def functions(text):
    matches=list(re.finditer(r'^function ([$\w]+)\(',text,re.M))
    if len({m[1] for m in matches})!=len(matches):raise ValueError('Duplicate function names')
    return {m[1]:text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)].rstrip() for i,m in enumerate(matches)}
def patch(text,replacements):
    matches=list(re.finditer(r'<script>(.*?)</script>',text,re.S))
    if len(matches)!=1:raise ValueError('Exactly one inline script is required')
    match=matches[0];script=match[1];a=script.index('function $(s)');b=script.index("\ndocument.addEventListener('keydown'")
    prefix=script[:a].replace('let state=normalizeState(loadState()||defaultState());',"const APP_VERSION='RC4 v0.24';\nlet storageState={lastRaw:null,error:'',notice:'',conflict:false,blocked:false,rawRecovery:null,runtimeError:null};\nlet toastTimer=null,lastScreenKey='';\nlet state=normalizeState(loadState()||defaultState());")
    old=functions(script[a:b]);old.update(replacements)
    old['chrome']=old['chrome'].replace('right=COURSE.version','right=APP_VERSION').replace('<button class="back" data-back>','<button class="back" data-back aria-label="\ub4a4\ub85c">')
    old['learnView']='function learnView(){const d=dailyById(state.activeDaily);if(!d)return learnHubView();const s=state.daily[d.id];if(!s||!Array.isArray(s.queue))return dailyIntroView(d.id);if(s.sessionDone||s.index>=s.queue.length)return s.completed?dailyEndView(d.id):sessionEndView(d.id);'+old['learnView'][old['learnView'].index('const item=s.queue'):]
    old['mockView']=old['mockView'].replace('reviewDone:false}', 'reviewDone:false,questionIds:MOCK.map(q=>q.id)}').replace("${sel===null?'disabled", "${!validPick(sel)?'disabled").replace('<div class="mock-footer"><button','<div class="mock-footer"><button class="btn" data-mock-prev ${m.index===0?\'disabled\':\'\'}>\uc774\uc804 \ubb38\ud56d</button><button')
    old['quickResultView']=old['quickResultView'].replace('\uac19\uc740 \ubb38\ud56d\uc740 \ub2e4\uc2dc \ucd9c\uc81c\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.','\uc9d1\uc911\ud559\uc2b5\uc740 \ubcc4\ub3c4\uc758 \uc804\uc6a9 \ubb38\uc81c\uad70\uc744 \uc0ac\uc6a9\ud569\ub2c8\ub2e4.')
    old['explanation']=old['explanation'].replace('2\ubb38\uc81c \ub4a4 \ub2e4\uc2dc','2\ubb38\uc81c \ub4a4 \u00b7 1\ud68c').replace('5\ubb38\uc81c \ub4a4 \ub2e4\uc2dc','5\ubb38\uc81c \ub4a4 \u00b7 1\ud68c')
    old['homeView']=old['homeView'].replace('\uc804\ub0a0 \uc624\ub2f5\uc774 \uc788\uc73c\uba74 \uac19\uc740 \uac1c\ub150\uc758 \ub2e4\ub978 \ubb38\ud56d\uc744 \uc6b0\uc120 \uc11e\uc2b5\ub2c8\ub2e4.','\uc804\uc6a9 \ubb38\uc81c\uad70 \uc548\uc5d0\uc11c \ucde8\uc57d \uac1c\ub150\uc744 \uc6b0\uc120 \ubcf5\uc2b5\ud569\ub2c8\ub2e4.')
    old['toolsView']=old['toolsView'].replace('\ud2c0\ub9b0 \uac1c\ub150\uc740 \ub2e4\uc74c\ub0a0 5\ubd84 \ubb38\uc81c\uc5d0 \ucd5c\ub300 6\uac1c\ub150\uae4c\uc9c0 \uc6b0\uc120 \ubc18\uc601\ud569\ub2c8\ub2e4.','5\ubd84 \ubb38\uc81c \uc804\uc6a9 \ubb38\ud56d\uc774 \uc788\ub294 \uac1c\ub150\uc740 1\ub2e8\uacc4\uc5d0\uc11c \ucd5c\ub300 6\uac1c\ub150\uae4c\uc9c0 \ud68c\ubcf5\ud569\ub2c8\ub2e4. \uc804\uc6a9 \ubb38\ud56d\uc774 \uc5c6\ub294 \uac1c\ub150\uc740 \ud574\ub2f9 Daily\uc758 \uc9d1\uc911\ud559\uc2b5\uc5d0\uc11c \ubcf5\uc2b5\ud569\ub2c8\ub2e4.')
    old['toolsView']=old['toolsView'].replace('<input type="file" id="importFile"','<button class="tool-btn" data-export-recovery>\ucd08\uae30\ud654\u00b7\uac00\uc838\uc624\uae30 \uc804 \uc6d0\ubcf8 \ubcf4\uad00\ubcf8</button><input type="file" id="importFile"')
    ending="</section></div>`,'tools')}"
    addition='</section>${reviewListHtml()}<section class="learn-card"><h3>\ubc84\uc804\u00b7\uc790\ub8cc \uae30\uc900</h3><p>${esc(COURSE.version)}<br>\uc2e4\uc81c \uc81c\uacf5 260\ubb38\ud56d \u00b7 \uc608\ube44 40\ubb38\ud56d \u00b7 Master 300\ubb38\ud56d\uc5d0 \uc608\ube44\ubb38\ud56d \ud3ec\ud568</p><p>\uc0ac\uc6a9\uc790 \uc81c\uacf5 \uacf5\uc2dd \uc790\ub8cc 10\uc885\uc744 \uae30\uc900\uc73c\ub85c \ud55c \ud559\uc2b5\uc6a9 \uc790\ub8cc\uc785\ub2c8\ub2e4. \ud604\ud589 \ubc95\ub839\u00b7\ub0b4\ubd80\uaddc\uc815\uc758 \ucd5c\uc2e0\uc131\uc744 \ubcf4\uc99d\ud558\uc9c0 \uc54a\uc73c\uba70, \uc2dc\ud5d8 \uc9c0\uc815 \uc790\ub8cc\uc640 \ud568\uaed8 \ud655\uc778\ud558\uc138\uc694.</p><p>\uae30\ub85d\uc740 \ud604\uc7ac \ube0c\ub77c\uc6b0\uc800\uc5d0 \ubcf4\uad00\ub429\ub2c8\ub2e4. \uae30\uae30\u00b7\ube0c\ub77c\uc6b0\uc800\u00b7\uc811\uc18d \uc8fc\uc18c\uac00 \ub2ec\ub77c\uc9c0\uba74 \uc790\ub3d9 \ub3d9\uae30\ud654\ub418\uc9c0 \uc54a\uc73c\ubbc0\ub85c JSON \ubc31\uc5c5\uc744 \uc774\uc6a9\ud558\uc138\uc694.</p></section></div>`,\'tools\')}'
    if ending not in old['toolsView']:raise ValueError('Tools anchor changed')
    old['toolsView']=old['toolsView'].replace(ending,addition)
    tail=r'''
document.addEventListener('keydown',e=>{
 if(e.repeat||e.ctrlKey||e.metaKey||e.altKey||['INPUT','TEXTAREA','SELECT','BUTTON','A'].includes(document.activeElement?.tagName)||document.activeElement?.isContentEditable)return;
 if(state.view==='quick'){if(['1','2','3','4'].includes(e.key)){e.preventDefault();answerQuick(Number(e.key)-1);}else if(e.key==='Enter'){e.preventDefault();nextQuick();}}
 else if(state.view==='learn'&&['1','2','3','4'].includes(e.key)){e.preventDefault();answerLearn(Number(e.key)-1);}
 else if(state.view==='mock'&&state.mock&&!state.mock.submitted){if(['1','2','3','4'].includes(e.key)){e.preventDefault();state.mock.answers[state.mock.index]=Number(e.key)-1;save();render();}else if(e.key==='Enter'){e.preventDefault();advanceMock();}}
});
window.addEventListener('storage',e=>{if(e.key===KEY&&e.newValue!==storageState.lastRaw){storageState.conflict=true;storageState.error='\ub2e4\ub978 \ucc3d\uc5d0\uc11c \uae30\ub85d\uc774 \ubcc0\uacbd\ub418\uc5c8\uc2b5\ub2c8\ub2e4. \uc774 \ucc3d\uc744 \ubc31\uc5c5\ud55c \ub4a4 \ucd5c\uc2e0 \uae30\ub85d\uc744 \ubd88\ub7ec\uc624\uc138\uc694.';render();}});
window.addEventListener('pagehide',()=>save());
render();
'''
    new_script=(prefix+'\n'.join(old.values())+'\n'+tail).replace('${q.question}','${esc(q.question)}')
    text=text[:match.start(1)]+new_script+text[match.end(1):]
    text=text.replace('RC4 v0.23','RC4 v0.24')
    css='''
/* v0.24 accessibility and storage status */
.storage-notice{padding:12px;margin:10px;border:1px solid #777;background:#f5f5f5;color:#222;font-size:14px;line-height:1.6}
.storage-notice button{margin:8px 8px 0 0;padding:9px;border:1px solid #777;border-radius:3px;background:#fff;color:#222;cursor:pointer}
.review-entry{padding:10px 0;border-top:1px solid #aaa}.review-entry p{margin:4px 0;font-size:.9em}
.hd h1{min-width:0}.hd .right{flex-shrink:0;max-width:45%}
button:focus-visible,[role="button"]:focus-visible{outline:3px solid currentColor;outline-offset:3px}
.mock-footer{display:flex;gap:10px}.mock-footer button{flex:1}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
'''
    text=text.replace('</style>',css+'</style>',1)
    text=text.replace('<body>','<body><noscript>\uc774 \ud559\uc2b5 \uc571\uc740 JavaScript\uac00 \ud544\uc694\ud569\ub2c8\ub2e4. \ube0c\ub77c\uc6b0\uc800 \uc124\uc815\uc744 \ud655\uc778\ud574 \uc8fc\uc138\uc694.</noscript>',1)
    return text

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--dest',type=Path);args=parser.parse_args();dest=args.dest or args.source
    replacements={}
    for module in sorted(Path(__file__).parent.glob('v024_*.js')):
        fs=functions(module.read_text(encoding='utf-8'))
        if replacements.keys()&fs.keys():raise ValueError('Duplicate module functions')
        replacements.update(fs)
    if 'normalizeState' not in replacements or 'render' not in replacements:raise ValueError('Missing module')
    outputs={}
    for name,sha in EXPECTED.items():
        raw=(args.source/name).read_bytes()
        if blob_sha(raw)!=sha:raise SystemExit('Input hash differs; stopped without writing: '+name)
        text=patch(raw.decode('utf-8'),replacements)
        if name=='03_INTRANET_PC.html':
            css='@media(min-width:900px){#app{filter:grayscale(1)}#app .main .flow-btn.strong,#app .main button.wide,#app .main button.strong,#app .main .primary,#app .main .btn.b-y{background:#e6e6e6!important;color:#333!important;border:1px solid #aaa!important}#app .main .study-num{background:#e0e0e0!important;color:#333!important}}'
            text=text.replace('</style>',css+'\n</style>',1)
        script=re.search(r'<script>(.*?)</script>',text,re.S)[1]
        with tempfile.NamedTemporaryFile(suffix='.js',mode='w',encoding='utf-8') as tmp:
            tmp.write(script);tmp.flush();subprocess.run(['node','--check',tmp.name],check=True)
        names=re.findall(r'^function ([$\w]+)\(',script,re.M)
        if len(names)!=len(set(names)):raise ValueError('Duplicate output function')
        outputs[name]=text.encode('utf-8')
    dest.mkdir(parents=True,exist_ok=True)
    for name,data in outputs.items():(dest/name).write_bytes(data);print(name,len(data),blob_sha(data))
if __name__=='__main__':main()
