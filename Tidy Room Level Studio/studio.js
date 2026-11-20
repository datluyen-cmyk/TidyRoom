import {Game} from './core/game.js';
import {createHash} from 'node:crypto';

export const hash=x=>createHash('sha256').update(typeof x==='string'?x:JSON.stringify(x)).digest('hex');
export const typeOf=id=>Number(id.split('-')[0]);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const avg=a=>a.length?a.reduce((s,x)=>s+x,0)/a.length:0;
const median=a=>a.length?[...a].sort((x,y)=>x-y)[a.length>>1]:0;
const rnd=(seed)=>()=>{seed|=0;seed=seed+0x6D2B79F5|0;let q=Math.imul(seed^seed>>>15,1|seed);q=q+Math.imul(q^q>>>7,61|q)^q;return((q^q>>>14)>>>0)/4294967296;};
const pick=(a,r)=>a[Math.min(a.length-1,Math.floor(r()*a.length))];
const shuffle=(a,r)=>{a=[...a]; for(let i=a.length-1;i>0;i--){let j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const n2=x=>+x.toFixed(3);
const sum=o=>Object.values(o).reduce((s,x)=>s+x,0);
function counts(a,key){const out={}; for(const x of a){const k=key(x);out[k]=(out[k]??0)+1}return out}
function inside(x,y,p){let c=false; for(let i=0,j=p.length-1;i<p.length;j=i++){const [a,b]=p[i],[d,e]=p[j];if((b>y)!==(e>y)&&x<(d-a)*(y-b)/(e-b)+a)c=!c}return c}
function pressure(game){return game.buffer.filter(s=>s.item).length}
function structure(l){const list=l.order.map(o=>o.type),streaks=[],qty=l.order.map(o=>o.count); const prev=new Map();list.forEach((t,i)=>{if(prev.has(t))streaks.push(i-prev.get(t));prev.set(t,i)});return {items:l.content.length,boxes:qty.length,groups:prev.size,meanBox:avg(qty),repeatGap:streaks.length?avg(streaks):qty.length,adjacent:streaks.filter(g=>g===1).length}}
function geometry(l,shapes){const game=new Game(l,shapes),free=game.items.filter((_,i)=>!game.isCovered(i)); const wanted=new Set(l.order.slice(0,2).map(x=>x.type));return {free:n2(free.length/l.content.length),direct:free.filter(x=>wanted.has(x.type)).length,contacts:n2(avg(game.items.map(x=>x.coverCandidates?.length??0)))}}
const predictors=['items','boxes','groups','meanBox','repeatGap','free','direct','contacts'];
const distance=(a,b,stats)=>Math.sqrt(avg(predictors.map(k=>((a[k]-b[k])/stats[k])**2)));
function predict(rows,f,stats,k=8){const near=rows.map(x=>[distance(f,x,stats),x.odds]).sort((a,b)=>a[0]-b[0]).slice(0,k);const w=near.map(x=>1/(.35+x[0]));return avg(near.map((x,i)=>x[1]*w[i]))/avg(w)}
export function fit(ref){const labeled=[];const targets=[];
 for(const l of ref.levels){const f={...structure(l),...geometry(l,ref.shapes)};const odds=ref.odds[l.level]??null; const row={level:l.level,sourceLevel:l.sourceLevel??l.level,family:l.bgFile,...f,odds,boxSizes:l.order.map(o=>o.count),typePattern:l.order.map(o=>o.type)};targets.push(row);if(odds!==null)labeled.push(row)}
 const stats=Object.fromEntries(predictors.map(k=>{const a=labeled.map(x=>x[k]),m=avg(a);return[k,Math.max(.05,Math.sqrt(avg(a.map(x=>(x-m)**2))))]}));
 const folds=[...new Set(labeled.map(x=>x.family))];const pred=[];for(const family of folds){const tr=labeled.filter(x=>x.family!==family),te=labeled.filter(x=>x.family===family);const s=Object.fromEntries(predictors.map(k=>{const a=tr.map(x=>x[k]),m=avg(a);return[k,Math.max(.05,Math.sqrt(avg(a.map(x=>(x-m)**2))))]}));for(const x of te)pred.push({level:x.level,expected:x.odds,estimate:n2(predict(tr,x,s)),baseline:median(tr.map(r=>r.odds))})}
 const mae=key=>n2(avg(pred.map(x=>Math.abs(x.expected-x[key]))));
 return {schema:1,algorithm:'empirical progression + constrained construction + polygon replay',targets,labeled,stats,validation:{referenceCount:targets.length,labeledCount:labeled.length,families:folds.length,proxy:'Packaged LEVEL_ODDS; meaning as observed human win rate is unverified.',mae:mae('estimate'),medianBaselineMAE:mae('baseline'),folds:pred},sourceHash:hash(ref)};
}

export function replay(level,items,path,{strict=false}={}){
 const g=new Game(level,items);const n=level.content.length;
 let peak=0,waits=0,overThree=0,forcedAtFull=0,early=0,windows=[];
 if(path.length!==n||new Set(path).size!==n||path.some(x=>!Number.isInteger(x)||x<0||x>=n))return {ok:false,reason:'invalid proof'};
 for(let i=0;i<path.length;i++){
  const u=path[i],pre=g.items.length;g.events=[];g.tapItem(u);
  if(g.items.length!==pre-1||g.events.some(x=>x.t==='blocked'))return {ok:false,reason:'blocked or invalid step',step:i,uid:u};
  const p=pressure(g);if(strict&&p>=5&&g.state!=='win')return {ok:false,reason:'strict tray full',step:i,uid:u};
  if(g.state==='fail')return {ok:false,reason:'out of space',step:i,uid:u};
  if(g.events.some(x=>x.t==='toBuffer')){waits++;if(i<n*.25)early++;}peak=Math.max(peak,p);overThree+=p>=3?1:0;forcedAtFull+=p>=5?1:0;
  if(i%10===9||i===n-1)windows.push({tap:i+1,waiting:p});
 }
 return {ok:g.state==='win'&&g.items.length===0&&!pressure(g),peak,waits,early,overThree,forcedAtFull,windows};
}

export function pointerReplay(level,items,path,{strict=false}={}){
 const g=new Game(level,items),points=[];let peak=0;
 for(const uid of path){
  const it=g.items.find(x=>x.uid===uid);if(!it||g.state!=='playing')return {ok:false,reason:'pointer replay stopped'};
  const {minX,maxX,minY,maxY}=it.aabb;let p;
  for(const n of [1,5,11]){for(let i=0;i<n*n;i++){
    const x=n2(minX+(maxX-minX)*((i%n)+.5)/n),y=n2(minY+(maxY-minY)*(Math.floor(i/n)+.5)/n);
    if(g.pickAt(x,y)===uid){p=[x,y];break;}
   }if(p)break;
  }
  if(!p)return {ok:false,reason:'no pointer point'};
  const n=g.items.length;g.events=[];g.tapAt(...p);if(g.items.length!==n-1)return {ok:false,reason:'pointer blocked'};
  peak=Math.max(peak,pressure(g));if(strict&&peak>=5)return {ok:false,reason:'pointer strict capacity'};
  points.push(p);
 }
 return {ok:g.state==='win'&&!g.items.length&&!pressure(g),peak,points};
}

function makeOrder(t,types,r,art,room){
 // Preserve quota distribution and unique group count. Shuffle box sizes; assign fresh groups with comparable repeat rhythm.
 const seen=new Set(),labels=shuffle(types,r).filter(x=>{const key=(art.types[x]??String(x)).trim().normalize('NFC').toLowerCase();if(seen.has(key))return false;seen.add(key);return true;}).slice(0,t.groups);
 if(labels.length<t.groups)throw Error(`Nền này chỉ đủ ${labels.length}/${t.groups} nhãn nhóm phân biệt.`);
 const rank=shuffle([...new Set(t.typePattern)],r),freq=counts(t.typePattern,x=>x),left=Object.fromEntries(labels.map((v,i)=>[v,freq[rank[i]]]));
 const order=[],sizes=shuffle(t.boxSizes,r),minGap=t.level<=2?1:Math.max(2,Math.round(t.repeatGap*.40));
 for(let j=0;j<t.boxes;j++){
  const possible=labels.filter(x=>left[x]>0);const safe=possible.filter(x=>!order.slice(-minGap).some(q=>q.type===x));
  const p=safe.length?safe:possible;
  const choices=p.map(x=>{const last=order.findLastIndex(y=>y.type===x);const gap=last<0?t.boxes:j-last;return {x,v:Math.min(t.repeatGap,gap)*.48+left[x]*2+r()*8-(last<0&&j>t.groups?2:0)}}).sort((a,b)=>b.v-a.v);
  const x=choices[0].x;left[x]--;order.push({type:x,count:sizes[j]});
 }
 return order;
}

function plannedTaps(order,r,target){
 // Independently plan two open receivers with a bounded number of deliberate future taps.
 const need={},waiting=[];for(const o of order)need[o.type]=(need[o.type]??0)+o.count;
 let next=0;const slots=[null,null],out=[];let budget=target.level===1?0:Math.max(1,Math.round(target.items*(target.odds>=60?.085:target.odds>=25?.145:.21)));
 const soft=target.level===1?0:target.level===2?2:target.odds===null?3:target.odds>=60?2:target.odds>=25?3:4;
 function fill(i){const q=order[next++];slots[i]=q?{...q,left:q.count}:null;if(!q)return;for(let j=0;j<waiting.length&&slots[i].left;){if(waiting[j]===q.type){waiting.splice(j,1);slots[i].left--}else j++}if(!slots[i].left)fill(i)}
 fill(0);fill(1);
 while(slots.some(Boolean)){
  const now=slots.filter(Boolean).map(s=>s.type),soon=order.slice(next,next+3).filter(q=>!now.includes(q.type)&&(need[q.type]??0)>0&&waiting.filter(x=>x===q.type).length<Math.max(1,q.count-1));
  if(budget>0&&out.length>=2&&waiting.length<soft&&soon.length&&r()<.25+(target.odds===null?.10:(100-target.odds)*.0025)){
   const t=pick(soon,r).type;out.push({type:t,wait:true});waiting.push(t);need[t]--;budget--;continue;
  }
  const a=slots.map((o,i)=>({o,i})).filter(x=>x.o&&need[x.o.type]>0);
  if(!a.length)throw Error('Không dựng được trình tự thu gom');
  const selected=a.length===1?a[0]:r()<.68?a.sort((u,v)=>u.o.left-v.o.left)[0]:pick(a,r);
  const t=selected.o.type;const dest=a.filter(x=>x.o.type===t).sort((u,v)=>(v.o.count-v.o.left)-(u.o.count-u.o.left)||u.i-v.i)[0];
  need[t]--;out.push({type:t,wait:false}); if(--dest.o.left===0)fill(dest.i);
 }
 return out;
}

function pose(id,shape,room,u,v,s,a,surface){return{id,x:n2((u-.5)*room.w),y:n2((.5-v)*room.h),scaleX:n2(s),scaleY:n2(s),angle:n2(a),surface}}
function fitRoom(room,items,steps,r,target,spreadBias){
 const groups={};for(const [id,art] of Object.entries(items))if(art.pose==='flat')(groups[art.type]??=[]).push(id);
 const roomZones=room.zones.map((z,i)=>({...z,index:i,rect:[Math.min(...z.poly.map(p=>p[0])),Math.min(...z.poly.map(p=>p[1])),Math.max(...z.poly.map(p=>p[0])),Math.max(...z.poly.map(p=>p[1]))]}));
 const centers=roomZones.map(()=>[]),anchors=shuffle(room.anchors??[],r);const placements=[]; const usedDrape=new Set();
 const groundSize=.48+Math.min(.21,steps.length*.0015);
 const centerCount=clamp(target.free*1.42*spreadBias,.17,.84);
 for(const step of steps){
  const choices=groups[step.type];
  const at=anchors.find(a=>!usedDrape.has(a.name)&&a.choices.some(c=>typeOf(c.id)===step.type));
  if(at&&placements.length>=Math.min(5,Math.floor(steps.length/4))){
   const c=pick(at.choices.filter(c=>typeOf(c.id)===step.type),r);usedDrape.add(at.name);placements.push(pose(c.id,items[c.id],room,at.u+(c.du??0),at.v+(c.dv??0),c.scale,c.angle,at.name));continue;
  }
  const zs=roomZones.filter(z=>!z.types||z.types.includes(step.type));
  let v=null;
  for(let rep=0;rep<85&&!v;rep++){
   let chance=r()*avg(zs.map(z=>z.weight??1))*zs.length, z=zs.find(z=>(chance-=z.weight??1)<=0)??zs[0];
   if(rep>25)z=zs[0];
   const id=pick(choices,r), art=items[id]; let sc=groundSize*(z.index===0?1:.87)*(.89+r()*.22);
   const [x0,y0,x1,y1]=z.rect;const existing=centers[z.index];const c=existing.length&&r()>centerCount?pick(existing,r):null;
   const u=c?c[0]+(r()-.5)*.085:x0+(x1-x0)*r(), w=c?c[1]+(r()-.5)*.073:y0+(y1-y0)*r();
   const angle=(r()-.5)*(z.index===0?64:34);if(rep>50)sc*=.78;
   const rx=(art.w*.40*sc+art.h*.20*sc*Math.abs(Math.sin(angle*Math.PI/180)))/room.w,ry=(art.h*.37*sc+art.w*.20*sc*Math.abs(Math.sin(angle*Math.PI/180)))/room.h;
   if(![[u,w],[u-rx,w],[u+rx,w],[u,w-ry],[u,w+ry]].every(([x,y])=>inside(x,y,z.poly)))continue;
   if(anchors.some(a=>Math.abs(a.u-u)<rx+.025&&Math.abs(a.v-w)<ry+.018))continue;
   if(!c)existing.push([u,w]);v=pose(id,art,room,u,w,sc,angle,z.label);
  }
  if(!v)throw Error(`Không đủ chỗ đặt nhóm ${step.type} trên ${room.label}`);placements.push(v);
 }
 // Earlier planned taps are drawn on top. This makes the witness legal for the actual polygons,
 // even if multiple overlapping neighbors combine to cover one sprite.
 return placements.reverse();
}

export function signature(l,items){
 const a=new Map();let n=0;
 const canonical=l.order.map(o=>{if(!a.has(o.type))a.set(o.type,n++);return[a.get(o.type),o.count]});
 const g=new Game(l,items);g.items.forEach((_,i)=>g.isCovered(i));
 // Ignore sprite paint, absolute coordinates/rotation and type names. Preserve cover topology and order pattern.
 const keys=g.items.map(x=>a.get(x.type));const graph=g.items.map((x,i)=>[keys[i],(x.coverCandidates??[]).map(y=>y.uid)]);
 return hash([canonical,graph]);
}

function scoreCandidate(f,t,proof){return Math.abs(f.free-t.free)*3.3+Math.abs(f.contacts-t.contacts)*.085+Math.abs(f.direct/Math.max(1,t.items)-t.direct/Math.max(1,t.items))*2+Math.abs(f.repeatGap-t.repeatGap)/Math.max(4,t.boxes)*1.2+f.adjacent*.20+(t.level===1&&proof.waits>0?1:0)}
export function generateOne(t,art,profile,seed,prev,opts={}){
 const r=rnd(seed),roomNames=Object.keys(art.rooms),roomKey=opts.room??roomNames[(t.level-1)%roomNames.length],room=art.rooms[roomKey];if(!room)throw Error('Không tìm thấy nền.');
 const attempts=opts.attempts??22;let best=null;const rejection={};
 const fail=k=>rejection[k]=(rejection[k]??0)+1;
 for(let k=0;k<attempts;k++)try{
  const order=makeOrder(t,room.types,r,art,room),steps=plannedTaps(order,r,t);if(steps.length!==t.items){fail('quota');continue;}
  const content=fitRoom(room,art.items,steps,r,t,.75+(k/(attempts-1||1))*.7);const level={level:t.level,name:`${room.label} ${t.level}`,bg:roomKey,bgFile:room.src,bgPosX:0,width:room.w,height:room.h,order,content};
  // Material art/data gates, not trained-score gates.
  if(Object.keys(counts(content,x=>typeOf(x.id))).length!==t.groups||order.length!==t.boxes||content.length!==t.items){fail('quota');continue}
  const have=counts(content,x=>typeOf(x.id)),q={};for(const o of order)q[o.type]=(q[o.type]??0)+o.count;
  if(Object.entries(q).some(([typ,count])=>count!==have[typ])){fail('quota');continue;}
  const path=content.map((_,i)=>content.length-1-i);const proof=replay(level,art.items,path,{strict:opts.strict});if(!proof.ok){fail(proof.reason);continue;}
  const f={...structure(level),...geometry(level,art.items)};
  // Wider tolerances for tiny rooms where 1–2 pieces materially change the ratio.
  if(Math.abs(f.free-t.free)>(t.items<40?.30:.235)||Math.abs(f.contacts-t.contacts)>Math.max(4,t.contacts*.9)||!f.direct){fail('reference geometry band');continue;}
  if(f.adjacent>Math.max(1,t.adjacent+1)){fail('adjacent duplicate');continue;}
  const sig=signature(level,art.items);if(prev.has(sig)){fail('equivalent structure');continue;}
  const estimate=profile.validation.mae<profile.validation.medianBaselineMAE?n2(predict(profile.labeled,f,profile.stats)):null;
  const s=scoreCandidate(f,t,proof)+(estimate!==null&&t.odds!==null?Math.abs(estimate-t.odds)*.003:0);
  if(!best||s<best.distance){const pointer=pointerReplay(level,art.items,path,{strict:opts.strict});if(!pointer.ok){fail(pointer.reason??'pointer does not win');continue;}best={level,path,points:pointer.points,proof,features:f,fingerprint:sig,distance:n2(s),attempt:k+1,seed,profileOdds:t.odds,estimateOdds:estimate}}
 }catch(e){fail(e.message);}
 return {best,rejection,attempts};
}

export function profiles(rows){return rows.map(x=>({level:x.level,items:x.items,boxes:x.boxes,groups:x.groups,free:x.free,direct:x.direct,contacts:x.contacts,repeatGap:x.repeatGap,odds:x.odds}))}

export function verifyTemplate(room,art){
 if(!room||!Array.isArray(room.zones)||!room.zones.length||room.zones.length>24||!Array.isArray(room.anchors)||room.anchors.length>20)throw Error('Cần ít nhất một vùng và tối đa 20 điểm neo.');
 if(room.zones[0].types)throw Error('Vùng đầu tiên phải dùng được cho tất cả nhóm đồ.');
 const number=x=>Number.isFinite(x)&&x>=0&&x<=1;
 const names=new Set();
 for(const z of room.zones){if(typeof z.label!=='string'||!z.label.trim()||names.has(z.label)||!Array.isArray(z.poly)||z.poly.length<3||z.poly.length>24||!z.poly.every(x=>Array.isArray(x)&&x.length===2&&x.every(number))||!Number.isFinite(z.weight??1)||(z.weight??1)<=0||(z.types&&(!z.types.length||z.types.some(t=>!room.types.includes(t)))))throw Error('Vùng đặt không hợp lệ.'); names.add(z.label)}
 for(const a of room.anchors){if(typeof a.name!=='string'||!a.name.trim()||names.has(a.name)||a.pose!=='drape'||!number(a.u)||!number(a.v)||!Array.isArray(a.choices)||!a.choices.length||a.choices.some(c=>{const s=art.items[c.id];return !s||s.pose!=='drape'||!Number.isFinite(c.angle)||Math.abs(c.angle)>180||!Number.isFinite(c.scale)||c.scale<.1||c.scale>2||Math.abs(c.du??0)>.25||Math.abs(c.dv??0)>.25||!number(a.u+(c.du??0))||!number(a.v+(c.dv??0));}))throw Error('Điểm vắt hoặc danh sách sprite không hợp lệ.'); names.add(a.name)}
 return room;
}
