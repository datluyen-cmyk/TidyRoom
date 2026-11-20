import {Game} from './core/game.js';
const $=id=>document.getElementById(id), ui=$('canvas'), ctx=ui.getContext('2d');
let art,model,pack,record,step=0,mode='layout',editing=false,drafts={},poll,drawTicket=0,selectedBatch='',playGame,strictFail=false,zoneDraft=null;
const img=new Map();
const loadImage=url=>{if(!img.has(url))img.set(url,new Promise((yes,no)=>{const a=new Image();a.onload=()=>yes(a);a.onerror=no;a.src=url}));return img.get(url)};
async function req(path,body){const r=await fetch(path,body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});const v=await r.json();if(!r.ok)throw Error(v.error??r.statusText);return v;}
function option(select,value,label){const o=document.createElement('option');o.value=value;o.textContent=label;select.append(o)}
function labelType(id){return art.types[id]??`Nhóm ${id}`}
const msg=(s,id='log')=>$(id).textContent=s;
function template(){const k=$('room').value,r=art.rooms[k];return r?drafts[k]??{zones:r.zones,anchors:r.anchors}:null}
function refreshEditor(){const t=template();$('template').value=t?JSON.stringify(t,null,2):'';$('moveAnchor').disabled=!t?.anchors?.length;$('apply').disabled=!t;$('reset').disabled=!t;$('downloadTemplate').disabled=!t;}
function persist(){try{localStorage.setItem('tidy-room-studio-template-v1',JSON.stringify(drafts));}catch{}}
function checkedDraft(obj){if(!obj||!Array.isArray(obj.zones)||!obj.zones.length||!Array.isArray(obj.anchors)||obj.zones.some(x=>!Array.isArray(x.poly)||x.poly.length<3||x.poly.some(p=>!Array.isArray(p)||p.length!==2||p.some(a=>!Number.isFinite(a)||a<0||a>1)))||obj.anchors.some(a=>!Array.isArray(a.choices)||!a.choices.length||!Number.isFinite(a.u)||!Number.isFinite(a.v)||a.choices.some(c=>!art.items[c.id]||!Number.isFinite(c.angle)||!Number.isFinite(c.scale))))throw Error('Kiểm tra vùng, tọa độ và ID sprite.');return {zones:obj.zones,anchors:obj.anchors};}

async function draw(){
 const ticket=++drawTicket,k=mode==='template'?$('room').value:record?.level.bg,room=art.rooms[k];
 const controls=mode==='layout'&&!!record;$('stepBack').disabled=!controls||step===0;$('stepNext').disabled=!controls||step===record?.path.length;$('resetSteps').disabled=!controls||step===0;
 $('play').disabled=!record;msg(mode==='play'?'Thoát chơi thử':'Chơi thử','play');
 msg(controls?`${step}/${record.path.length} lần lấy`:'','stepLabel');
 const hud=$('hud');hud.replaceChildren();$('boxes').style.display=mode==='layout'?'flex':'none';
 if(mode==='play'&&playGame){
  const entries=[...playGame.orders.filter(o=>o.open&&o.type>=0).map(o=>`${labelType(o.type)} ${o.count}/${o.total}`),`Khay ${playGame.buffer.filter(x=>x.item).length}/5`,...playGame.buffer.filter(b=>b.item).map(b=>labelType(b.item.type))];
  if(playGame.state!=='playing'||strictFail)entries.push(playGame.state==='win'?'Đã dọn sạch!':'Hết chỗ. Bấm Thoát và Chơi thử để thử lại.');
  entries.forEach(x=>{const el=document.createElement('span');el.textContent=x;hud.append(el)});
 }
 if(!room){ctx.clearRect(0,0,ui.width,ui.height);return;}
 try{
  const background=await loadImage(room.src);
  const t=template(), hide=new Set(record?.path?.slice(0,step)??[]);const visible=mode==='layout'&&record?record.level.content.map((c,i)=>({...c,i})).filter(c=>!hide.has(c.i)):mode==='play'&&playGame?playGame.items.map(c=>({...c,i:c.uid})):[];
  const draws=await Promise.all(visible.map(async c=>[c,await loadImage(art.items[c.id].src)]));if(ticket!==drawTicket)return;
  const size=900/Math.max(room.w,room.h);ui.width=Math.round(room.w*size);ui.height=Math.round(room.h*size);
  ctx.setTransform(size,0,0,size,0,0);ctx.drawImage(background,0,0,room.w,room.h);
  if(mode==='template'&&t){
   const colors=['#257253','#ca712f','#6565b4','#a43e5b'];
   t.zones.forEach((z,i)=>{const c=colors[i%colors.length];ctx.beginPath();z.poly.forEach(([u,v],j)=>ctx[j?'lineTo':'moveTo'](u*room.w,v*room.h));ctx.closePath();ctx.fillStyle=c+'33';ctx.strokeStyle=c;ctx.lineWidth=4/size;ctx.fill();ctx.stroke();const [x,y]=z.poly[0];ctx.font=`${16/size}px system-ui`;ctx.fillStyle=c;ctx.fillText(z.label,x*room.w+8/size,y*room.h+17/size);});
   t.anchors.forEach(a=>{ctx.beginPath();ctx.arc(a.u*room.w,a.v*room.h,9/size,0,2*Math.PI);ctx.fillStyle='#e04030';ctx.strokeStyle='white';ctx.lineWidth=2/size;ctx.fill();ctx.stroke();ctx.font=`${15/size}px system-ui`;ctx.fillStyle='#611708';ctx.fillText(a.name,a.u*room.w+13/size,a.v*room.h+5/size)});
   if(zoneDraft?.length){ctx.beginPath();zoneDraft.forEach(([u,v],i)=>ctx[i?'lineTo':'moveTo'](u*room.w,v*room.h));if(zoneDraft.length>=3)ctx.closePath();ctx.lineWidth=4/size;ctx.strokeStyle='#8f286b';ctx.stroke();}
  }
  const next=record?.path[step];
  for(const [c,image] of draws){const s=art.items[c.id];ctx.save();ctx.translate(room.w/2+c.x,room.h/2-c.y);ctx.rotate(-c.angle*Math.PI/180);ctx.scale(c.scaleX,c.scaleY);ctx.drawImage(image,-s.w/2,-s.h/2,s.w,s.h);if(mode==='layout'&&step>0&&c.i===next){ctx.strokeStyle='#ffe663';ctx.lineWidth=4/size/c.scaleX;ctx.strokeRect(-s.w/2,-s.h/2,s.w,s.h)}ctx.restore()}
 }catch{if(ticket===drawTicket)msg('Không tải được ảnh xem trước.','viewNote')}
}

function renderRecord(){
 record=pack?.records[Number($('levels').value)]??null;step=0;mode='layout';editing=false;stopZone();
 msg(record?`Mốc ${record.level.level} — ${art.rooms[record.level.bg].label}`:'Xem bố cục','viewTitle');
 $('boxes').replaceChildren();if(record)record.level.order.forEach(o=>{const s=document.createElement('span');s.textContent=labelType(o.type)+' × '+o.count;$('boxes').append(s)});
 msg(record?'Xem thứ tự hộp và đường giải; không mô phỏng chuyển động trong game.':'Chọn lượt đã sinh để xem bố cục.','viewNote');
 const m=$('metrics');m.replaceChildren();if(record){
  const t=document.createElement('table'); const vals=[['Thông số','RoomSort','Màn sinh'],['Đồ / hộp / nhóm',`${record.target.items} / ${record.target.boxes} / ${record.target.groups}`,`${record.features.items} / ${record.features.boxes} / ${record.features.groups}`],['Đồ lấy được lúc đầu',`${Math.round(record.target.free*100)}%`,`${Math.round(record.features.free*100)}%`],['Slot chờ cao nhất theo đường giải','—',`${record.proof.peak}/5`],['Số lượt đưa vào slot chờ','—',record.proof.waits],['Nhãn odds / ước tính (tham khảo)',record.target.odds??'—',record.estimateOdds??'—']];
  vals.forEach((r,i)=>{const tr=t.insertRow();r.forEach(v=>{const c=document.createElement(i?'td':'th');c.textContent=v;tr.append(c)})});m.append(t);
 }draw();
}
async function openBatch(id,keep=false){
 selectedBatch=id;if(!id){pack=null;renderRecord();return;}
 const prefix=`batches/${encodeURIComponent(id)}/`;let latest=null;
 for(const f of ['pack.json','partial.json','checkpoint.json'])try{latest=await req(prefix+f);break}catch{}
 if(selectedBatch!==id)return;pack=latest;const old=$('levels').value;$('levels').replaceChildren();$('downloads').replaceChildren();
 if(pack){pack.records.forEach((x,i)=>option($('levels'),i,`Mốc ${x.level.level}`));if(keep&&old!==''&&Number(old)<pack.records.length)$('levels').value=old;
  const files=pack.status==='complete'?[['levels.json','Tải level JSON'],['pack.json','Lời giải + thông số'],['progression.csv','Bảng progression'],['validation.json','Báo cáo']]:[['checkpoint.json','Điểm lưu hiện tại']];
  if(['incomplete','cancelled'].includes(pack.status))files.push(['partial.json','Các màn chạy qua'],['validation.json','Báo cáo']);
  files.forEach(([f,label])=>{const a=document.createElement('a');a.href=prefix+f;a.download=f;a.textContent=label;$('downloads').append(a)})
 }renderRecord();
}
async function refreshBatches(preferred){const v=await req('/api/batches');const h=$('batches');const old=preferred??h.value;h.replaceChildren();option(h,'','Chọn lượt đã sinh');for(const b of v)option(h,b,b);h.value=v.includes(old)?old:v[0]??'';if(h.value)await openBatch(h.value);}

async function update(){try{
 const j=await req('/api/status'), worked=j.log.filter(a=>a.phase==='checked'), p=j.log.at(-1);$('startJob').disabled=j.active;$('stop').disabled=!j.active;
 if(p){$('progress').max=p.count;$('progress').value=worked.length;const missing=worked.filter(p=>!p.passed).map(x=>x.level).join(', ');msg(j.error?j.error:j.result?`${j.result.status==='complete'?'Hoàn tất':j.result.status==='cancelled'?'Đã dừng':'Chưa đủ màn'}: ${p.accepted}/${p.count} màn đạt.${missing?' Mốc chưa đạt: '+missing+'.':''}`:`Đang xét mốc ${p.level??'…'} · ${p.accepted}/${p.count} màn đạt.`);}
 else if(j.error){msg(j.error)}
 if(!j.active){clearInterval(poll);poll=null;if(j.result)await refreshBatches(j.result.batchName)}
 }catch(e){msg(e.message);}}

async function init(){
 [art,model]=await Promise.all([req('/data/art.json'),req('/data/model.json')]);
 for(const [k,r] of Object.entries(art.rooms))option($('room'),k,r.label);
 try{drafts=JSON.parse(localStorage.getItem('tidy-room-studio-template-v1')||'{}')}catch{}
 $('room').onchange=()=>{stopZone();refreshEditor();if(mode==='template')draw()};
 $('templateMode').onclick=()=>{stopZone();if(!$('room').value)$('room').value=Object.keys(art.rooms)[0];refreshEditor();mode='template';editing=false;msg(art.rooms[$('room').value].label+' — vùng đặt và điểm vắt','viewTitle');draw()};
 $('moveAnchor').onclick=()=>{if(!template()?.anchors?.length)return;$('templateMode').click();editing=true;msg('Click vào ảnh để dời điểm vắt đầu tiên.','editorMsg')};
 $('drawZone').onclick=()=>{$('templateMode').click();zoneDraft=[];$('zoneTools').classList.remove('hide');msg('Click các góc theo thứ tự quanh vùng, rồi bấm Lưu vùng.','editorMsg');};
 $('cancelZone').onclick=()=>{stopZone();draw();};
 $('saveZone').onclick=()=>{const k=$('room').value,t=structuredClone(template()),label=$('zoneName').value.trim();if(!zoneDraft||zoneDraft.length<3||zoneDraft.length>24||!label||t.zones.some(z=>z.label===label)||t.anchors.some(z=>z.name===label)){msg('Cần 3–24 điểm và tên vùng chưa trùng.','editorMsg');return;}t.zones.push({label,poly:zoneDraft,weight:.12});drafts[k]=t;persist();stopZone();refreshEditor();draw();msg('Đã thêm vùng. Có thể giới hạn nhóm đồ trong JSON.','editorMsg');};
 ui.onclick=e=>{const r=ui.getBoundingClientRect(),u=(e.clientX-r.left)/r.width,v=(e.clientY-r.top)/r.height;
  if(mode==='play'&&playGame?.state==='playing'&&!strictFail){const b=record.level;playGame.events=[];playGame.tapAt((u-.5)*b.width,(.5-v)*b.height);if(playGame.events.some(x=>x.t==='blocked'))msg('Món này đang bị đè. Lấy đồ phía trên trước.','viewNote');else msg('Chơi thử luật và bố cục, chưa có animation / booster.','viewNote');strictFail=pack.strict&&playGame.buffer.filter(x=>x.item).length>=5&&playGame.state!=='win';draw();return;}
  if(mode==='template'&&zoneDraft){if(zoneDraft.length<24)zoneDraft.push([+u.toFixed(4),+v.toFixed(4)]);draw();return;}
  if(mode!=='template'||!editing)return;const k=$('room').value,t=structuredClone(template());t.anchors[0].u=+(Math.max(0,Math.min(1,u))).toFixed(4);t.anchors[0].v=+(Math.max(0,Math.min(1,v))).toFixed(4);drafts[k]=t;persist();editing=false;refreshEditor();draw();msg('Đã dời điểm vắt. Lượt sinh cho nền này sẽ dùng template vừa chỉnh.','editorMsg');};
 $('apply').onclick=()=>{try{drafts[$('room').value]=checkedDraft(JSON.parse($('template').value));persist();refreshEditor();$('templateMode').click();msg('Đã áp dụng template cho lượt sinh tiếp theo.','editorMsg')}catch(e){msg(e.message,'editorMsg')}};
 $('reset').onclick=()=>{delete drafts[$('room').value];persist();refreshEditor();draw();msg('Đã khôi phục nền mẫu.','editorMsg')};
 $('downloadTemplate').onclick=()=>{const t=template();if(!t)return;const a=document.createElement('a');const url=URL.createObjectURL(new Blob([JSON.stringify(t,null,2)],{type:'application/json'}));a.href=url;a.download=$('room').value+'-template.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1500)};
 $('levels').onchange=renderRecord;$('batches').onchange=()=>openBatch($('batches').value);$('stepBack').onclick=()=>{step=Math.max(0,step-1);draw()};$('stepNext').onclick=()=>{if(record){step=Math.min(record.path.length,step+1);draw()}};$('resetSteps').onclick=()=>{step=0;draw()};
 $('play').onclick=()=>{if(!record)return;if(mode==='play'){renderRecord();return;}mode='play';strictFail=false;playGame=new Game(record.level,art.items);msg('Chạm một món trên ảnh để lấy. Chế độ này không dùng booster.','viewNote');draw()};
 $('startJob').onclick=async()=>{try{const opts={start:Number($('start').value),count:Number($('count').value),seed:Number($('seed').value),room:$('room').value,strict:$('strict').checked,exclude:$('exclusion').checked};if(!Number.isInteger(opts.start)||!Number.isInteger(opts.count)||opts.start<1||opts.count<1||opts.start+opts.count-1>model.targets.length||!Number.isSafeInteger(opts.seed))throw Error('Kiểm tra mốc, số màn và seed.');
  if(opts.room&&drafts[opts.room])opts.template=drafts[opts.room];$('startJob').disabled=true;await req('/api/start',opts);$('stop').disabled=false;$('progress').value=0;msg('Đang khởi tạo lượt sinh…');if(poll)clearInterval(poll);poll=setInterval(update,650);update();}catch(e){msg(e.message);$('startJob').disabled=false;}};
 $('stop').onclick=async()=>{await req('/api/stop',{});$('stop').disabled=true;msg('Đang dừng sau mốc hiện tại…');};
 refreshEditor();await refreshBatches();msg('Sẵn sàng. 130 mốc tham chiếu, 3 nền Tidy Room.');const j=await req('/api/status');if(j.active){poll=setInterval(update,650);update();}
}
function stopZone(){zoneDraft=null;$('zoneTools').classList.add('hide');}
init().catch(e=>msg('Không khởi động được: '+e.message));
