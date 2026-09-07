function isRecord(x){return x!==null&&typeof x==='object'&&!Array.isArray(x)&&(Object.getPrototypeOf(x)===Object.prototype||Object.getPrototypeOf(x)===null)}
function integer(x,min=0,max=1000000,fallback=0){const n=Number(x);return Number.isFinite(n)?Math.max(min,Math.min(max,Math.floor(n))):fallback}
function validPick(x){return Number.isInteger(x)&&x>=0&&x<4}
function safeDate(x,fallback=localDayKey()){return typeof x==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&!Number.isNaN(new Date(x+'T12:00:00').getTime())&&localDayKey(new Date(x+'T12:00:00'))===x?x:fallback}
function uniqueIds(x,allowed){return Array.isArray(x)?[...new Set(x.filter(id=>typeof id==='string'&&allowed.has(id)))]:[]}
function normalizeState(input){
  const s=isRecord(input)?input:{},next=reviewDefaultState();
  const allowed=new Set(QUESTIONS.map(q=>q.id)),dailyIds=new Set(DAILIES.map(d=>d.id));
  const ratings=new Set(['again','hard','good','easy']);
  const stats=isRecord(s.questionStats)?s.questionStats:{};
  for(const q of QUESTIONS){const x=stats[q.id];if(!isRecord(x))continue;const attempts=integer(x.attempts),pick=validPick(x.lastPick)?x.lastPick:null;next.questionStats[q.id]={attempts,correct:integer(x.correct,0,attempts),lastPick:pick,lastRating:ratings.has(x.lastRating)?x.lastRating:null,lastCorrect:typeof x.lastCorrect==='boolean'?x.lastCorrect:(attempts>0&&pick!==null?pick===q.answer:null),lastAttemptAt:typeof x.lastAttemptAt==='string'?x.lastAttemptAt.slice(0,40):null};}
  const incomingDaily=isRecord(s.daily)?s.daily:{},legacyDone=new Set();
  for(const x of Object.values(incomingDaily))if(isRecord(x))for(const id of uniqueIds(x.done,allowed))legacyDone.add(id);
  for(const d of DAILIES){
    const x=isRecord(incomingDaily[d.id])?incomingDaily[d.id]:{},ids=new Set(focusQuestionIds(d));
    const done=uniqueIds(s.dailySchemaVersion===DAILY_SCHEMA_VERSION?x.done:[...legacyDone],ids);
    const oldQueue=Array.isArray(x.queue)?x.queue:[],oldIndex=integer(x.index,0,oldQueue.length),queue=[],counts={};let index=0;
    if(s.dailySchemaVersion===DAILY_SCHEMA_VERSION&&s.flowSchemaVersion===FLOW_SCHEMA_VERSION){oldQueue.slice(0,1000).forEach((item,i)=>{if(!isRecord(item)||!ids.has(item.qid)||(counts[item.qid]||0)>=2)return;counts[item.qid]=(counts[item.qid]||0)+1;queue.push({qid:item.qid,isReview:item.isReview===true,repeat:item.repeat===true||counts[item.qid]>1,recovery:item.recovery===true});if(i<oldIndex)index++;});}
    const sessionDone=x.sessionDone===true||index>=queue.length;
    const pick=validPick(x.pick)?x.pick:null,answered=!sessionDone&&x.answered===true&&pick!==null;
    const repeats={};for(const item of queue)if(item.repeat)repeats[item.qid]=1;
    next.daily[d.id]={done,completed:ids.size>0&&done.length===ids.size,queue,index,sessionDone,answered,pick:answered?pick:null,baseCount:queue.filter(item=>!item.isReview).length,repeats,startCoverage:integer(x.startCoverage,0,100),endCoverage:integer(x.endCoverage,0,100)};
  }
  const settings=isRecord(s.settings)?s.settings:{};
  next.settings={mode:settings.mode==='time'?'time':'count',count:settings.count==='all'?'all':integer(settings.count,20,80,DEFAULT_FOCUS_COUNT),minutes:integer(settings.minutes,40,160,DEFAULT_FOCUS_MINUTES)};
  if(!Object.prototype.hasOwnProperty.call(settings,'count'))next.settings.count=DEFAULT_FOCUS_COUNT;
  if(!Object.prototype.hasOwnProperty.call(settings,'minutes'))next.settings.minutes=DEFAULT_FOCUS_MINUTES;
  const bank=isRecord(s.reviewBank)?s.reviewBank:{};
  for(const c of CONCEPTS){const x=bank[c.id];if(!isRecord(x))continue;const ids=new Set(conceptQids(c.id));const correctQids=uniqueIds(x.correctQids,ids);let status=['DUE','RECOVERING','MASTERED'].includes(x.status)?x.status:'DUE';if(status==='MASTERED'&&(correctQids.length<2||ids.size<2))status='RECOVERING';next.reviewBank[c.id]={concept:c.id,category:c.area,seedQid:ids.has(x.seedQid)?x.seedQid:[...ids][0],lastWrongQid:ids.has(x.lastWrongQid)?x.lastWrongQid:null,lastWeakQid:ids.has(x.lastWeakQid)?x.lastWeakQid:null,lastServedQid:ids.has(x.lastServedQid)?x.lastServedQid:null,lastPick:validPick(x.lastPick)?x.lastPick:null,source:['quick','focus','review','mock','self'].includes(x.source)?x.source:'self',wrongCount:integer(x.wrongCount),selfWeakCount:integer(x.selfWeakCount),correctStreak:integer(x.correctStreak),correctQids,status,dueOn:safeDate(x.dueOn),seenQids:uniqueIds(x.seenQids,ids),updatedAt:typeof x.updatedAt==='string'?x.updatedAt.slice(0,40):null};}
  const oldFlow=s.flowSchemaVersion===FLOW_SCHEMA_VERSION;
  const q=isRecord(s.quick)?s.quick:null;
  if(oldFlow&&q&&Array.isArray(q.queue)&&q.queue.length===QUICK_REQUIRED_COUNT&&uniqueIds(q.queue,QUICK_SET).length===QUICK_REQUIRED_COUNT){
    const answers=[];for(let i=0;i<q.queue.length;i++){const a=Array.isArray(q.answers)?q.answers[i]:null;if(!isRecord(a)||a.qid!==q.queue[i]||!validPick(a.pick))break;answers.push({qid:a.qid,pick:a.pick,ok:a.pick===questionById(a.qid).answer,recovery:Array.isArray(q.recoveryIds)&&q.recoveryIds.includes(a.qid)});}
    let index=integer(q.index,0,QUICK_REQUIRED_COUNT);index=Math.min(index,answers.length);const answered=index<QUICK_REQUIRED_COUNT&&!!answers[index];const done=index===QUICK_REQUIRED_COUNT&&answers.length===QUICK_REQUIRED_COUNT;
    next.quick={queue:q.queue.slice(),answers,recoveryIds:uniqueIds(q.recoveryIds,new Set(q.queue)),index,answered,pick:answered?answers[index].pick:null,done,detail:['why','source'].includes(q.detail)?q.detail:'',startedAt:typeof q.startedAt==='string'?q.startedAt.slice(0,40):null};
  }
  const gate=isRecord(s.focusGate)?s.focusGate:{};
  next.focusGate={ready:gate.ready===true&&next.quick?.done===true,pendingDailyId:dailyIds.has(gate.pendingDailyId)?gate.pendingDailyId:null,completedAt:typeof gate.completedAt==='string'?gate.completedAt.slice(0,40):null};
  const run=isRecord(s.focusRun)?s.focusRun:null;
  if(oldFlow&&run){const target=integer(run.target,1,FOCUS_TOTAL,DEFAULT_FOCUS_COUNT);next.focusRun={active:run.active===true,target,done:integer(run.done,0,target),mode:run.mode==='review'?'review':'learn',completedQids:uniqueIds(run.completedQids,allowed),startedAt:typeof run.startedAt==='string'?run.startedAt.slice(0,40):null,completedAt:typeof run.completedAt==='string'?run.completedAt.slice(0,40):null,startDailyId:dailyIds.has(run.startDailyId)?run.startDailyId:null};if(next.focusRun.done>=target)next.focusRun.active=false;}
  const m=isRecord(s.mock)?s.mock:null;
  if(oldFlow&&m&&(!m.questionIds||(Array.isArray(m.questionIds)&&m.questionIds.join('|')===MOCK.map(q=>q.id).join('|')))){
    const answers=MOCK.map((q,i)=>Array.isArray(m.answers)&&validPick(m.answers[i])?m.answers[i]:null),submitted=m.submitted===true&&answers.every(validPick);
    next.mock={index:integer(m.index,0,MOCK.length-1),answers,submitted,reviewIndex:integer(m.reviewIndex,0,MOCK.length),reviewDone:submitted&&m.reviewDone===true,reviewRecorded:submitted&&m.reviewRecorded===true,questionIds:MOCK.map(q=>q.id)};
  }
  next.studyDate=safeDate(s.studyDate);next.activeDaily=dailyIds.has(s.activeDaily)?s.activeDaily:null;
  next.view=['home','learnHub','quick','dailyIntro','learn','dailyEnd','sessionEnd','map','planner','mock','tools'].includes(s.view)?s.view:'home';next.toast='';
  if(next.view==='quick'&&!next.quick)next.view='learnHub';
  if(['dailyIntro','learn','dailyEnd','sessionEnd'].includes(next.view)&&!next.activeDaily)next.view='learnHub';
  if(next.view==='learn'){const ds=next.daily[next.activeDaily];if(!ds?.queue.length||ds.sessionDone)next.view=ds?.completed?'dailyEnd':'dailyIntro';}
  return next;
}
