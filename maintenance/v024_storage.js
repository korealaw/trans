function loadState(){
  try{
    const raw=localStorage.getItem(KEY);storageState.lastRaw=raw;if(!raw)return null;
    let parsed;
    try{parsed=JSON.parse(raw);if(!isRecord(parsed))throw new Error('invalid state');}
    catch(e){storageState.rawRecovery=raw;try{localStorage.setItem(KEY+'_corrupt_backup',raw);storageState.notice='손상된 기록의 원문을 보존했습니다. 기록 메뉴에서 복구용 파일을 받으세요.';}catch(b){storageState.blocked=true;storageState.error='손상된 원본 기록을 보호하기 위해 저장을 중지했습니다.';}return null;}
    const malformed=(parsed.questionStats!==undefined&&!isRecord(parsed.questionStats))||(parsed.daily!==undefined&&!isRecord(parsed.daily))||(parsed.reviewBank!==undefined&&!isRecord(parsed.reviewBank))||(isRecord(parsed.daily)&&Object.values(parsed.daily).some(ds=>!isRecord(ds)||(ds.done!==undefined&&!Array.isArray(ds.done))||(ds.queue!==undefined&&!Array.isArray(ds.queue))));
    if(malformed){storageState.rawRecovery=raw;storageState.notice='손상된 기록의 원문을 보관하고 읽을 수 있는 기록을 복구했습니다.';try{localStorage.setItem(KEY+'_corrupt_backup',raw);}catch(e){storageState.blocked=true;}}
    if(parsed.flowSchemaVersion>FLOW_SCHEMA_VERSION||parsed.dailySchemaVersion>DAILY_SCHEMA_VERSION){storageState.blocked=true;storageState.rawRecovery=raw;storageState.error='더 새로운 앱에서 저장한 기록입니다. 덮어쓰지 않고 보호합니다. 앱을 업데이트해 주세요.';}
    return parsed;
  }catch(e){storageState.error='자동 저장을 사용할 수 없습니다. 창을 닫기 전 기록을 내보내세요.';return null;}
}
function save(){
  if(storageState.blocked||storageState.conflict)return false;
  try{const current=localStorage.getItem(KEY);if(current!==storageState.lastRaw){storageState.conflict=true;storageState.error='다른 창에서 기록이 변경되었습니다. 이 창을 백업한 뒤 최신 기록을 불러오세요.';return false;}const raw=JSON.stringify(state);localStorage.setItem(KEY,raw);storageState.lastRaw=raw;storageState.error='';return true;}
  catch(e){storageState.error='자동 저장에 실패했습니다. 용량·저장 설정을 확인하고 기록을 내보내세요.';return false;}
}
function toast(msg){clearTimeout(toastTimer);state.toast=msg;render();toastTimer=setTimeout(()=>{state.toast='';render();},2500);}
function downloadJson(value,name){const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'}),a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);}
function exportProgress(){downloadJson({courseId:COURSE.id,version:COURSE.version,datasetId:'active260-v023-order1',exportedAt:new Date().toISOString(),state},'MG_learning_progress_'+localDayKey()+'.json');}
function exportRecovery(){let raw=storageState.rawRecovery;try{raw=raw||localStorage.getItem(KEY+'_recovery_backup')||localStorage.getItem(KEY+'_corrupt_backup');}catch(e){}if(!raw){toast('복구용 원본이 없습니다.');return;}let payload;try{payload=JSON.parse(raw);if(!isRecord(payload)||payload.courseId!==COURSE.id||!isRecord(payload.state))throw new Error('raw');}catch(e){payload={courseId:COURSE.id,recoveryRaw:raw,exportedAt:new Date().toISOString()};}downloadJson(payload,'MG_learning_recovery_'+localDayKey()+'.json');}
function backupProgress(reason){localStorage.setItem(KEY+'_recovery_backup',JSON.stringify({courseId:COURSE.id,datasetId:'active260-v023-order1',exportedAt:new Date().toISOString(),backupReason:reason,state}));}
function validateImport(p){
  if(!isRecord(p)||p.courseId!==COURSE.id)throw new Error('다른 과정이거나 백업 형식이 아닙니다.');
  if(p.datasetId&&p.datasetId!=='active260-v023-order1')throw new Error('다른 문제은행 버전입니다.');
  const s=p.state;if(!isRecord(s)||!isRecord(s.questionStats)||!isRecord(s.daily))throw new Error('학습기록 구조가 손상되었습니다.');
  if(s.flowSchemaVersion>FLOW_SCHEMA_VERSION||s.dailySchemaVersion>DAILY_SCHEMA_VERSION)throw new Error('더 새로운 앱에서 만든 기록입니다. 앱을 업데이트해 주세요.');
  if(s.reviewBank!==undefined&&!isRecord(s.reviewBank))throw new Error('오답 기록 형식이 올바르지 않습니다.');
  for(const ds of Object.values(s.daily))if(!isRecord(ds)||(ds.done!==undefined&&!Array.isArray(ds.done))||(ds.queue!==undefined&&!Array.isArray(ds.queue)))throw new Error('Daily 기록이 손상되었습니다.');
  return normalizeState(s);
}
function importProgress(ev){
  const f=ev.target.files?.[0];ev.target.value='';if(!f)return;if(f.size>5*1024*1024){alert('백업 파일은 5MB 이하만 가져올 수 있습니다.');return;}
  const r=new FileReader();r.onerror=()=>alert('파일을 읽지 못했습니다.');r.onload=()=>{
    try{const candidate=validateImport(JSON.parse(r.result));if(!confirm('현재 기록을 자동 백업한 뒤, 선택한 파일로 교체할까요?'))return;if(storageState.conflict||storageState.blocked)throw new Error('먼저 저장 충돌을 해결해 주세요.');backupProgress('before_import');const before=state;state=candidate;state.view='home';if(!save()){state=before;render();throw new Error('저장하지 못해 기존 기록을 유지했습니다.');}toast('학습기록을 불러왔습니다.');}catch(e){alert('가져오기 실패: '+e.message);}
  };r.readAsText(f);
}
function resetProgress(){
  if(!confirm('기존 기록을 복구용으로 보관하고 학습기록을 초기화할까요?'))return;
  try{if(storageState.conflict||storageState.blocked)throw new Error('저장 충돌을 먼저 해결해 주세요.');backupProgress('before_reset');const old=state;state=defaultState();if(!save()){state=old;throw new Error('저장할 수 없어 초기화하지 않았습니다.');}render();}catch(e){alert(e.message);}
}
function loadLatestProgress(){if(!confirm('이 창의 미저장 변경을 대체합니다. 필요한 기록을 내보냈나요?'))return;storageState.conflict=false;storageState.blocked=false;storageState.error='';state=normalizeState(loadState()||defaultState());state.view='home';render();}
function storageBanner(){const text=storageState.error||storageState.notice;if(!text)return '';return `<section class="storage-notice" role="alert"><strong>${esc(text)}</strong><div><button type="button" data-export>기록 내보내기</button>${storageState.conflict?'<button type="button" data-load-latest>최신 기록 불러오기</button>':''}</div></section>`;}
