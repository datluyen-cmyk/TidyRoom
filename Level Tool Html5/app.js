import {Playtest, sorted, check, itemAt, ROUND} from './game.js';

const $=id=>document.getElementById(id), canvas=$('board'), ctx=canvas.getContext('2d');
const create=(tag,txt,cls)=>{const e=document.createElement(tag);if(txt!==undefined)e.textContent=txt;if(cls)e.className=cls;return e};
const btn=(label,fn,title)=>{const b=create('button',label);b.onclick=fn;if(title)b.title=title;return b};
const option=(value,label)=>{const o=create('option',label);o.value=value;return o};
const clone=obj=>structuredClone(obj);
const normalize=s=>s.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu,'').replaceAll('đ','d');
const slug=s=>normalize(s).replace(/[^a-z0-9_-]+/g,'-').replace(/^[-_]+|[-_]+$/g,'').slice(0,65)||'level';
const assetURL=key=>'/asset/'+key.split('/').map(encodeURIComponent).join('/');
const say=s=>{$('notice').textContent=s};
let catalog,level=null,assetLookup=new Map(),groupNames=new Map(),batch=null,batchPos=-1,selected=null,pending=null,game=null,playingLoad=false;
let history=[],future=[],kind='items',assetPage=0,showGrid=true,inspector='layer',space=false,drag=null,flash=null;
let paletteGesture=null,ghost=null,idSerial=0;
let view={zoom:1,dx:0,dy:0}, dims={w:0,h:0,s:1,cx:0,cy:0},savedTimer,frame=0,busyImport=false;
const images=new Map(),masks=new Map(),maskJobs=new Map();
const boundsOnly=new Map();
const ready=()=>!!level;

async function api(url,body){
  const q=await fetch(url,body===undefined?{}:{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
  const data=await q.json();if(!q.ok)throw Error(data.error||q.statusText);return data;
}
function getImage(key){
  if(!images.has(key)){const img=new Image();img.onload=schedule;img.src=assetURL(key);images.set(key,img)}return images.get(key);
}
function thumb(key,alt=''){const i=create('img');i.src=assetURL(key);i.alt=alt;i.loading='lazy';return i}
function getMask(key){
  if(masks.has(key))return Promise.resolve(masks.get(key));
  if(!maskJobs.has(key))maskJobs.set(key,api('/api/shape?asset='+encodeURIComponent(key)).then(m=>{masks.set(key,m);return m}).finally(()=>maskJobs.delete(key)));
  return maskJobs.get(key);
}
function warmMasks(){for(const key of new Set(level.items.map(x=>x.asset)))getMask(key).catch(()=>{});}

const openStore=new Promise((resolve,reject)=>{const q=indexedDB.open('tidy-html5-level-tool',1);q.onupgradeneeded=()=>q.result.createObjectStore('draft');q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error)});
async function readDraft(){const db=await openStore;return new Promise((resolve,reject)=>{const q=db.transaction('draft').objectStore('draft').get('current');q.onsuccess=()=>resolve(q.result);q.onerror=()=>reject(q.error)});}
function saveSoon(){clearTimeout(savedTimer);savedTimer=setTimeout(async()=>{try{const db=await openStore;const tx=db.transaction('draft','readwrite');tx.objectStore('draft').put({level,batch,batchPos},'current');}catch{}},350);}
function download(name,doc){const file=new Blob([JSON.stringify(doc,null,2)],{type:'application/json'}),url=URL.createObjectURL(file),a=create('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}

function newLevel(){
  const bg=catalog.backgrounds.find(b=>b.path==='Art/TidyRoomBG/bedroom.jpg')||catalog.backgrounds[0];
  return {schema:'tidy-level-tool/1',key:'man-moi',name:'Màn mới',rule:'strict',background:{asset:bg.path,width:bg.w,height:bg.h,cameraX:0},items:[],boxes:[]};
}
function openLevel(doc,position=-1){
  level=doc;batchPos=position;selected=null;pending=null;paletteGesture=null;ghost=null;game=null;history=[];future=[];drag=null;flash=null;view={zoom:1,dx:0,dy:0};
  $('title').value=level.name;render();warmMasks();saveSoon();
}
function patch(fn){
  const before=clone(level);fn();if(JSON.stringify(before)===JSON.stringify(level))return;
  stash(before);render();saveSoon();
}
function stash(before){history.push(before);if(history.length>35)history.shift();future=[]}
function rewind(back){
  if(game||!level)return;const src=back?history:future,dest=back?future:history;if(!src.length)return;
  dest.push(level);level=src.pop();$('title').value=level.name;if(!level.items.some(i=>i.uid===selected))selected=null;
  render();warmMasks();saveSoon();
}
function setSelection(uid){selected=uid;renderPanel();schedule();}
const item=()=>level?.items.find(i=>i.uid===selected);
function syncBatch(){if(batch&&batchPos>=0)batch.levels[batchPos]=level;}
function newItemId(){
  let id;
  do{ id=globalThis.crypto?.randomUUID?.()??`local-${Date.now().toString(36)}-${++idSerial}`; }
  while(level.items.some(it=>it.uid===id));
  return id;
}

function renderPlacement(){
  const active=pending&&!game&&kind==='items';
  $('modeTip').hidden=!active;
  $('placeCenter').hidden=!active;
  canvas.classList.toggle('placing',!!active);
  if(active)$('modeTip').textContent=`Đang đặt ${pending.id} · Bấm vị trí hoặc nhấn Esc`;
  for(const tile of $('assetList').querySelectorAll('[data-sprite]')){
    const isSelected=tile.dataset.path===pending?.path;
    tile.classList.toggle('active',isSelected);tile.setAttribute('aria-pressed',String(isSelected));
  }
}

function drawPalette(reset=false){
  if(reset)assetPage=0;
  const family=$('family').value, search=normalize($('search').value.trim());
  const isItems=kind==='items';$('itemsTab').classList.toggle('active',isItems);$('bgTab').classList.toggle('active',!isItems);
  const coll=catalog[kind].filter(x=>family==='all'||x.family===family);
  const filter=$('groupFilter'), old=filter.value;
  filter.hidden=!isItems;
  if(isItems){
    const groups=new Map(coll.filter(a=>a.group!==null).map(a=>[a.group,a.label]));
    filter.replaceChildren(option('','Tất cả nhóm'),...[...groups].sort((a,b)=>a[1].localeCompare(b[1],'vi')).map(([key,label])=>option(key,`${label} · ${key}`)));
    if(groups.has(Number(old))&&old!=='')filter.value=old;
  }
  const entries=coll.filter(a=>(!isItems||!filter.value||+filter.value===a.group)&&normalize(`${a.id} ${a.label}`).includes(search));
  const pages=Math.max(1,Math.ceil(entries.length/48));assetPage=Math.min(assetPage,pages-1);
  const list=$('assetList');list.replaceChildren();
  for(const a of entries.slice(assetPage*48,assetPage*48+48)){
    const tile=btn('',e=>{if(!e.detail||!tile.suppressClick)chooseArt(a);},`${a.id} · ${a.label}${isItems?' · Kéo vào phòng hoặc chọn rồi bấm vị trí':''}`);
    tile.className='asset-card'+(!isItems&&level?.background.asset===a.path?' active':'');
    const icon=thumb(a.path);icon.draggable=false;
    tile.dataset.path=a.path;tile.append(icon,create('span',isItems?a.id:a.label));list.append(tile);
    if(isItems){
      tile.dataset.sprite='';tile.onpointerdown=e=>{
        if(e.button!==0||!e.isPrimary||!ready()||game||playingLoad)return;
        tile.suppressClick=false;
        paletteGesture={a,tile,target:level,id:e.pointerId,sx:e.clientX,sy:e.clientY,moved:false};
        tile.setPointerCapture(e.pointerId);
      };
      tile.ondragstart=e=>e.preventDefault();
    }
  }
  if(!entries.length)list.append(create('span','Không tìm thấy asset.','empty'));
  $('assetPage').textContent=`${assetPage+1}/${pages} · ${entries.length}`;$('assetPrev').disabled=assetPage===0;$('assetNext').disabled=assetPage+1>=pages;
  renderPlacement();
}

function chooseArt(a){
  if(!ready()||playingLoad)return;
  if(game){say('Bấm Về xếp đồ để thay đổi level.');return}
  if(kind==='backgrounds'){
    pending=null;ghost=null;patch(()=>{level.background={asset:a.path,width:a.w,height:a.h,cameraX:0}});view={zoom:1,dx:0,dy:0};drawPalette();schedule();say('Đã đổi nền. Tọa độ đồ giữ nguyên theo tâm.');return;
  }
  pending=a;getImage(a.path);getMask(a.path).catch(()=>{});renderPlacement();schedule();
  say(`Đã chọn ${a.id}. Bấm vị trí trên nền hoặc kéo thẻ đồ vào phòng. Esc để dừng đặt.`);
}
function referenceSize(a,bg,imageSize){
  const p=catalog.placement,ref=p?.sizes[a.path],ratio=ref?.rooms[bg.asset]||ref?.default;
  if(ratio)return {w:ROUND(bg.height*ratio[0]),h:ROUND(bg.height*ratio[1])};
  const d=imageSize||masks.get(a.path)||(()=>{const img=getImage(a.path);return img.naturalWidth?{w:img.naturalWidth,h:img.naturalHeight}:null;})();
  if(!d)return null;
  const src=p?.roomShapes[a.id];
  const k=a.family==='happy'?(p?.happyScales[assetLookupBgId(bg.asset)]?.[a.group]??1)*bg.height/2640:
    (src?Math.min(src[0]/d.w,src[1]/d.h):a.family==='tidy'?.48:.50)*bg.height/1560;
  return {w:ROUND(d.w*k),h:ROUND(d.h*k)};
}
const assetLookupBgId=asset=>asset.split('/').at(-1).replace(/\.[^.]+$/,'');
async function sizeFor(a,bg){return referenceSize(a,bg)||referenceSize(a,bg,await getMask(a.path));}
async function place(p,a,targetLevel){
  try{
    if(level!==targetLevel||game||playingLoad)return;
    const m=referenceSize(a,level.background)||await sizeFor(a,level.background);
    if(level!==targetLevel||game||playingLoad)return;
    const group=a.group??0;const linked=level.boxes.find(o=>o.group===group);
    const same=level.items.find(i=>i.group===group);
    patch(()=>{
      const uid=newItemId();level.items.push({uid,asset:a.path,group,targetType:linked?.targetType??same?.targetType??group,layer:Math.max(-1,...level.items.map(i=>i.layer))+1,x:p.x,y:p.y,width:m.w,height:m.h,angle:0,scaleX:1,scaleY:1});selected=uid;
    });
    const b=level.background,outside=Math.abs(p.x)>b.width/2||Math.abs(p.y)>b.height/2;
    say(`Đã đặt ${a.id} · X ${p.x} / Y ${p.y}${outside?' · Ngoài mép nền':''}. ${pending?'Bấm để đặt tiếp hoặc nhấn Esc.':'Kéo đồ trên nền để chỉnh vị trí.'}`);
  }catch(e){say(`Không đặt được ${a.id}: ${e.message}`)}
}
async function resetSize(items){
  if(!items.length||game||playingLoad)return;
  const target=level,bg=level.background;
  try{
    const sizes=await Promise.all(items.map(async it=>[it,await sizeFor(assetLookup.get(it.asset),bg)]));
    if(level!==target||level.background!==bg||game)return;
    const live=new Set(level.items);
    patch(()=>{for(const [it,d] of sizes)if(live.has(it)){
      it.width=d.w;it.height=d.h;it.scaleX=Math.sign(it.scaleX);it.scaleY=Math.sign(it.scaleY);
    }});
    say(`Đã đưa ${items.length} món về cỡ tham chiếu. Có thể Hoàn tác.`);
  }catch(e){say(`Không lấy được cỡ đồ: ${e.message}`);}
}
function renderBatch(){
  $('batchbar').hidden=!batch||game!==null;if(!batch)return;
  const select=$('batchLevel');if(select.options.length!==batch.levels.length)select.replaceChildren(...batch.levels.map((l,i)=>option(i,`${i+1}. ${l.name} · ${l.items.length} món`)));
  if(batchPos>=0){select.value=batchPos;select.options[batchPos].textContent=`${batchPos+1}. ${level.name} · ${level.items.length} món`;}
}
function label(group){return groupNames.get(group)??`Nhóm ${group}`}
function knownGroups(){
  const keys=new Set([...groupNames.keys(),...level.items.map(i=>i.group),...level.boxes.map(b=>b.group)]);
  return [...keys].sort((a,b)=>label(a).localeCompare(label(b),'vi')||a-b);
}
function groupSelect(select,preset,prefer,preserve=false){
  const activeGroups=[...new Set([...level.items.map(i=>i.group),...level.boxes.map(b=>b.group)])];
  const ids=prefer?[...activeGroups,...knownGroups().filter(k=>!activeGroups.includes(k))]:knownGroups();
  const signature=ids.join(',');
  if(select.dataset.signature!==signature){select.replaceChildren(...ids.map(k=>option(k,`${label(k)} · ${k}`)));select.dataset.signature=signature;}
  if(preset!==undefined&&(!preserve||!select.value))select.value=preset;
}
function renderPanel(){
  if(!level)return;
  const it=item();$('summary').textContent=`${level.items.length} món · ${level.boxes.length} hộp`;
  $('fitAll').disabled=!level.items.length||!!game;
  $('layerPanel').hidden=inspector!=='layer';$('boxPanel').hidden=inspector!=='box';
  $('layerTab').classList.toggle('active',inspector==='layer');$('boxTab').classList.toggle('active',inspector==='box');
  if(inspector==='layer'){
    $('selectionEmpty').hidden=!!it;$('itemFields').hidden=!it;$('itemFields').disabled=!!game;
    if(it){
      $('itemTitle').textContent=assetLookup.get(it.asset)?.id||it.asset;
      for(const k of ['x','y','angle','scaleX','scaleY'])$(k).value=it[k];
      groupSelect($('itemGroup'),it.group,true);
      const ids=sorted(level.items).map(i=>i.uid);$('layerBack').disabled=ids[0]===it.uid;$('layerFront').disabled=ids.at(-1)===it.uid;
    }
    const ul=$('layers'),y=ul.scrollTop;ul.replaceChildren();
    for(const i of sorted(level.items).reverse()){
      const b=btn('',()=>{pending=null;ghost=null;renderPlacement();setSelection(i.uid)},`X ${i.x} / Y ${i.y}`);b.className='layer'+(selected===i.uid?' active':'');
      b.dataset.uid=i.uid;b.append(thumb(i.asset),create('span',assetLookup.get(i.asset)?.id||i.asset,'grow'),create('small',`L${i.layer}`));ul.append(b);
    }ul.scrollTop=y;
  }else{
    $('rule').value=level.rule;$('rule').disabled=!!game;
    const orders=$('orders');orders.replaceChildren();
    level.boxes.forEach((o,i)=>{
      const row=create('div',undefined,'sort-row'), count=create('input');count.type='number';count.min='1';count.max='3000';count.value=o.count;count.disabled=!!game;
      count.setAttribute('aria-label',`Sức chứa hộp ${i+1}`);count.onchange=()=>{const n=Math.max(1,Math.min(3000,Math.round(+count.value||1)));patch(()=>o.count=n);count.value=n;};
      const actions=create('div',undefined,'sort-actions'),up=btn('↑',()=>moveBox(i,-1),'Đưa hộp lên'),down=btn('↓',()=>moveBox(i,1),'Đưa hộp xuống'),del=btn('×',()=>patch(()=>level.boxes.splice(i,1)),'Bỏ hộp');
      up.disabled=!!game||i===0;down.disabled=!!game||i===level.boxes.length-1;del.disabled=!!game;actions.append(up,down,del);
      row.append(create('small',i+1),create('span',o.label),count,actions);orders.append(row);
    });
    groupSelect($('groupOrder'),level.items[0]?.group,true,true);$('groupOrder').disabled=$('addBox').disabled=$('fillBoxes').disabled=!!game;
    const report=check(level);$('validation').classList.toggle('invalid',!report.ok);
    $('validation').textContent=report.ok?'Đủ chỗ cho từng nhóm. Có thể chơi thử hoặc xuất Unity.':!level.items.length?'Đặt đồ trước, sau đó tạo hộp.':report.deltas.map(x=>`${label(x.group)}: ${x.have} đồ / ${x.want} chỗ`).join(' · ');
  }
}
function render(){
  if(!level)return;
  $('title').disabled=!!game;$('editorMode').textContent=game?'02 / PLAYTEST':'02 / XẾP LEVEL';
  $('play').textContent=game?'■ Dừng test':'▶ Playtest';
  $('undo').disabled=!!game||!history.length;$('redo').disabled=!!game||!future.length;
  $('playbar').hidden=!game;$('grid').hidden=!!game;
  for(const k of ['new','library','unity','download'])$(k).disabled=!!game;
  renderPlacement();
  if(!game)$('finish').hidden=true;
  syncBatch();renderBatch();renderPanel();if(game)renderPlay();schedule();
}
function arrange(offset){
  const it=item();if(!it||game)return;const all=sorted(level.items),i=all.indexOf(it),j=i+offset;if(j<0||j>=all.length)return;
  patch(()=>{[it.layer,all[j].layer]=[all[j].layer,it.layer]});
}
function moveBox(i,offset){const j=i+offset;patch(()=>{[level.boxes[i],level.boxes[j]]=[level.boxes[j],level.boxes[i]]})}
function removeItem(){const it=item();if(it&&!game)patch(()=>{level.items=level.items.filter(i=>i!==it);selected=null});}
function duplicate(){const it=item();if(!it||game)return;patch(()=>{selected=newItemId();level.items.push({...it,uid:selected,x:it.x+20,y:it.y-20,layer:Math.max(...level.items.map(i=>i.layer))+1})});}

function schedule(){if(!frame)frame=requestAnimationFrame(()=>{frame=0;draw()});}
function makeTransform(w,h){
  const b=level.background,s=Math.min(Math.max(1,w-44)/b.width,Math.max(1,h-40)/b.height)*view.zoom;
  return {w,h,s,cx:w/2+view.dx,cy:h/2+view.dy};
}
const world=(x,y)=>[(x-dims.cx)/dims.s,(dims.cy-y)/dims.s];
const screen=(x,y)=>[dims.cx+x*dims.s,dims.cy-y*dims.s];
function draw(){
  if(!level)return;const w=canvas.clientWidth,h=canvas.clientHeight,dpr=window.devicePixelRatio||1;
  if(!w||!h)return;
  if(canvas.width!==Math.round(w*dpr)||canvas.height!==Math.round(h*dpr)){canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr)}
  dims=makeTransform(w,h);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,w,h);
  const {s,cx,cy}=dims,b=level.background,bg=getImage(b.asset);
  const x=cx-b.width*s/2,y=cy-b.height*s/2,bw=b.width*s,bh=b.height*s;
  ctx.fillStyle='#dfd4bc';ctx.fillRect(x,y,bw,bh);
  if(bg.complete&&bg.naturalWidth)ctx.drawImage(bg,x,y,bw,bh);
  ctx.strokeStyle='#ffffff6e';ctx.strokeRect(x,y,bw,bh);
  if(showGrid&&!game){
    ctx.save();ctx.beginPath();ctx.rect(x,y,bw,bh);ctx.clip();const n=s*100;
    if(n>=12){ctx.strokeStyle='#ffffff38';ctx.beginPath();for(let a=cx% n;a<w;a+=n){ctx.moveTo(a,0);ctx.lineTo(a,h)}for(let a=cy%n;a<h;a+=n){ctx.moveTo(0,a);ctx.lineTo(w,a)}ctx.stroke()}
    ctx.strokeStyle='#2e7a61cc';ctx.setLineDash([6,4]);ctx.beginPath();ctx.moveTo(cx,y);ctx.lineTo(cx,y+bh);ctx.moveTo(x,cy);ctx.lineTo(x+bw,cy);ctx.stroke();ctx.restore();
    ctx.fillStyle='#24634b';ctx.beginPath();ctx.arc(cx,cy,3.5,0,Math.PI*2);ctx.fill();
  }
  const items=game?game.items:sorted(level.items);
  items.forEach((it,j)=>{
    if(game&&!game.room.has(j))return;let [px,py]=screen(it.x,it.y);
    if(flash?.uid===it.uid){const age=performance.now()-flash.at;if(age<280){px+=Math.sin(age/13)*4;schedule()}else flash=null;}
    const img=getImage(it.asset);ctx.save();ctx.translate(px,py);ctx.rotate(-it.angle*Math.PI/180);ctx.scale(it.scaleX,it.scaleY);
    const iw=it.width*s,ih=it.height*s;
    if(img.complete&&img.naturalWidth)ctx.drawImage(img,-iw/2,-ih/2,iw,ih);
    if(!game&&selected===it.uid){ctx.strokeStyle='#123b2b';ctx.lineWidth=2/Math.max(Math.abs(it.scaleX),Math.abs(it.scaleY));ctx.strokeRect(-iw/2-2,-ih/2-2,iw+4,ih+4);ctx.strokeStyle='#baf2cf';ctx.setLineDash([4,4]);ctx.strokeRect(-iw/2-2,-ih/2-2,iw+4,ih+4)}
    ctx.restore();
  });
  const preview=paletteGesture?.moved?paletteGesture.a:pending;
  if(preview&&ghost&&!game&&!drag&&kind==='items'){
    const img=getImage(preview.path);
    const [gx,gy]=screen(ghost.x,ghost.y);
    const d=referenceSize(preview,level.background);
    if(img.naturalWidth&&d){
      const w=d.w*s,h=d.h*s;
      ctx.save();ctx.globalAlpha=.65;ctx.drawImage(img,gx-w/2,gy-h/2,w,h);ctx.restore();
    }
    ctx.save();ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.beginPath();ctx.arc(gx,gy,8,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  $('zoomText').textContent=`${Math.round(view.zoom*100)}%`;
}
const pointer=e=>{const r=canvas.getBoundingClientRect();return {sx:e.clientX-r.left,sy:e.clientY-r.top};};
function pointForPlacement(e){
  const r=canvas.getBoundingClientRect(),d=makeTransform(r.width,r.height);
  const x=(e.clientX-r.left-d.cx)/d.s,y=(d.cy-e.clientY+r.top)/d.s;
  return e.shiftKey?{x:Math.round(x/25)*25,y:Math.round(y/25)*25}:{x:ROUND(x),y:ROUND(y)};
}
function overBoard(e){
  const r=canvas.getBoundingClientRect();
  return e.clientX>=r.left&&e.clientX<r.right&&e.clientY>=r.top&&e.clientY<r.bottom;
}
document.addEventListener('pointermove',e=>{
  const g=paletteGesture;if(!g||e.pointerId!==g.id)return;
  if(!g.moved&&Math.hypot(e.clientX-g.sx,e.clientY-g.sy)<5)return;
  if(!g.moved){g.moved=true;chooseArt(g.a);}
  ghost=overBoard(e)?pointForPlacement(e):null;
  schedule();
},true);
function endPalette(e,cancel=false){
  const g=paletteGesture;if(!g||e.pointerId!==g.id)return;
  paletteGesture=null;ghost=null;
  if(!g.moved)return;
  g.tile.suppressClick=true;
  pending=null;renderPlacement();schedule();
  if(!cancel&&g.target===level&&overBoard(e))place(pointForPlacement(e),g.a,g.target);
  else if(!cancel)say('Thả đồ trong khu vực xếp level để đặt.');
}
document.addEventListener('pointerup',endPalette,true);
document.addEventListener('pointercancel',e=>endPalette(e,true),true);
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('pointerdown',e=>{
  if(!level||playingLoad)return;const {sx,sy}=pointer(e),[x,y]=world(sx,sy);
  const pan=e.button===1||e.button===2||space;
  if(pan){drag={type:'pan',sx,sy,dx:view.dx,dy:view.dy};canvas.classList.add('panning');}
  else if(e.button!==0)return;
  else if(game){tap(x,y);return;}
  else{
    const stack=sorted(level.items),found=itemAt(stack,x,y,masks)||itemAt(stack,x,y,boundsOnly);setSelection(found?.uid??null);
    const placement=kind==='items'?pending:null;
    if(found)drag={type:'item',uid:found.uid,sx,sy,ox:found.x,oy:found.y,before:clone(level),moved:false,placement};
    else if(placement)drag={type:'place',placement};
    else return;
  }
  canvas.setPointerCapture(e.pointerId);e.preventDefault();
});
canvas.addEventListener('pointermove',e=>{
  if(!level)return;const {sx,sy}=pointer(e),[x,y]=world(sx,sy);$('coord').textContent=`X ${Math.round(x)} · Y ${Math.round(y)}`;
  if(!drag){if(pending&&kind==='items'&&!game){ghost=pointForPlacement(e);schedule();}return;}
  if(drag.type==='pan'){view.dx=drag.dx+sx-drag.sx;view.dy=drag.dy+sy-drag.sy;}
  else if(drag.type==='item'&&(drag.moved||Math.hypot(sx-drag.sx,sy-drag.sy)>4)){
    const a=item();if(!a)return;drag.moved=true;let px=drag.ox+(sx-drag.sx)/dims.s,py=drag.oy-(sy-drag.sy)/dims.s;
    if(pending){pending=null;ghost=null;renderPlacement();}
    if(e.shiftKey){px=Math.round(px/25)*25;py=Math.round(py/25)*25;}
    a.x=ROUND(px);a.y=ROUND(py);$('x').value=a.x;$('y').value=a.y;
  }
  schedule();
});
canvas.addEventListener('pointerleave',()=>{ghost=null;schedule();});
function endDrag(e,cancel=false){
  const g=drag;drag=null;canvas.classList.remove('panning');
  if(g?.type==='item'&&g.moved){if(cancel)level=g.before;else{stash(g.before);saveSoon();}render();}
  else if(!cancel&&g?.placement&&overBoard(e)){ghost=null;place(pointForPlacement(e),g.placement,level);}
}
canvas.addEventListener('pointerup',e=>endDrag(e));canvas.addEventListener('pointercancel',e=>endDrag(e,true));
canvas.addEventListener('wheel',e=>{
  if(!level)return;e.preventDefault();const {sx,sy}=pointer(e),[x,y]=world(sx,sy);
  view.zoom=Math.max(.32,Math.min(8,view.zoom*Math.exp(-e.deltaY*.0018)));
  const d=makeTransform(dims.w,dims.h);view.dx=sx-d.w/2-x*d.s;view.dy=sy-d.h/2+y*d.s;schedule();
},{passive:false});
new ResizeObserver(schedule).observe($('viewport'));

async function startPlay(){
  if(!level||playingLoad)return;if(game){game=null;render();say('Đã về chế độ xếp đồ.');return;}
  if(!check(level).ok){inspector='box';renderPanel();say('Số chỗ trong hộp phải khớp số đồ của từng nhóm. Xem mục Hộp & luật.');return;}
  playingLoad=true;say('Đang nạp viền sprite để playtest…');
  try{
    const target=level;await Promise.all([...new Set(level.items.map(i=>i.asset))].map(getMask));if(level!==target)return;
    pending=null;paletteGesture=null;ghost=null;selected=null;game=new Playtest(clone(level),masks);render();drawPalette();say('Bấm đồ không bị đè để dọn. Có 2 hộp mở và 5 slot chờ.');
  }catch(e){say(e.message)}finally{playingLoad=false;}
}
function renderPlay(){
  const boxes=$('testBoxes'),tray=$('testTray');boxes.replaceChildren();tray.replaceChildren();
  for(const b of game.boxes){
    const card=create('div',undefined,'test-box'), icon=create('div',undefined,'box-art'), o=game.order(b);
    if(catalog.ui.GP_Box0)icon.style.backgroundImage=`url("${assetURL(catalog.ui.GP_Box0)}")`;
    if(o){const it=game.items.find(i=>i.group===o.group);if(it)icon.append(thumb(it.asset));}
    const text=create('div');text.append(create('strong',o?.label||'Đã xong'),create('div',o?`${b.count}/${o.count}`:''));card.append(icon,text);boxes.append(card);
  }
  for(let i=0;i<5;i++){const cell=create('div',undefined,'slot');cell.title=`Slot chờ ${i+1}`;
    if(catalog.ui.GP_Slot)cell.style.backgroundImage=`url("${assetURL(catalog.ui.GP_Slot)}")`;
    if(game.tray[i]!==undefined)cell.append(thumb(game.items[game.tray[i]].asset));tray.append(cell);
  }
  const done=$('finish');done.hidden=game.state==='playing';
  if(!done.hidden)done.replaceChildren(create('strong',game.state==='win'?'Đã dọn sạch!':'Hết chỗ trong khay'),create('div',`${game.moves} lượt · Khay cao nhất ${game.peak}/5`),btn('Chơi lại',restart));
}
function restart(){if(!game)return;game=new Playtest(clone(level),masks);flash=null;renderPlay();schedule();say('Đã bắt đầu lại màn.');}
function tap(x,y){const r=game.tapAt(x,y);
  if(r.kind==='blocked'){flash={uid:game.items[r.j].uid,at:performance.now()};say('Món này đang bị đè. Dọn món phía trên trước.');}
  else if(r.kind==='full')say('Khay đầy. Hãy lấy món vào thẳng hộp đang mở.');
  else if(r.kind==='box'||r.kind==='tray')say(`${game.room.size} món trên nền · ${game.tray.length}/5 slot chờ · ${game.delivered}/${game.items.length} đã vào hộp.`);
  renderPlay();schedule();
}

function setLibrary(entries){$('unityLevel').replaceChildren(...entries.map(e=>option(e.key,`${e.label} · ${e.source}`)));}
function openReport(){
  if(!batch)return;const fail=batch.rejected||[],warnings=batch.levels.flatMap(l=>(l.origin?.warnings||[]).map(w=>({file:l.name,error:w})));
  $('reportSummary').textContent=`${batch.levels.length} màn nhập được · ${fail.length} lỗi đọc · ${warnings.length} lưu ý`;
  $('reportRows').replaceChildren(...[...fail,...warnings].map(r=>create('div',`${r.file}${r.level?' · '+r.level:''}: ${r.error}`,'report-row')));
  $('reportDialog').showModal();
}
async function importPack(job){
  if(busyImport)return;busyImport=true;$('importStatus').textContent='Đang chuyển level và kiểm tra asset…';
  for(const k of ['loadOne','allUnity','allRoom','allHappy'])$(k).disabled=true;
  try{
    const p=await job();
    if(!p.levels.length){
      const first=p.rejected.slice(0,3).map(x=>`${x.file}: ${x.error}`).join('\n');$('importStatus').textContent=`Không nhập được màn nào.\n${first}`;
      if(p.rejected.length){const b=btn('Tải báo cáo lỗi',()=>download('import-report.json',p));$('importStatus').append(document.createElement('br'),b);}return;
    }
    batch=p;$('batchLevel').replaceChildren();openLevel(clone(p.levels[0]),0);drawPalette();$('loadDialog').close();
    say(`Đã nhập ${p.levels.length} màn${p.rejected.length?` · ${p.rejected.length} lỗi` : ''}. Chọn màn ở hàng phía trên.`);
    if(p.rejected.length)openReport();
  }catch(e){$('importStatus').textContent=e.message;}finally{
    busyImport=false;for(const k of ['loadOne','allUnity'])$(k).disabled=false;
    $('allRoom').disabled=!catalog.sources.roomsort;$('allHappy').disabled=!catalog.sources.happy;
  }
}
function source(kind,key=''){return importPack(()=>api(`/api/library?source=${kind}&key=${encodeURIComponent(key)}`));}
const encodeFile=file=>new Promise((ok,no)=>{const r=new FileReader();r.onload=()=>ok(String(r.result).split(',')[1]);r.onerror=()=>no(r.error);r.readAsDataURL(file);});
function importFiles(files){
  const selectedFiles=[...files].filter(f=>/\.(json(?:\.gz)?|zip)$/i.test(f.name));
  if(!selectedFiles.length){$('importStatus').textContent='Không tìm thấy JSON, JSON.GZ hoặc ZIP.';return;}
  if(selectedFiles.length>2000||selectedFiles.reduce((n,f)=>n+f.size,0)>96*1024*1024){$('importStatus').textContent='Tối đa 2000 file / 96 MB mỗi lượt.';return;}
  importPack(async()=>api('/api/convert',{mode:$('source').value,files:await Promise.all(selectedFiles.map(async f=>({name:f.webkitRelativePath||f.name,data:await encodeFile(f)})))}));
}

function bind(){
  for(const k of ['itemsTab','bgTab'])$(k).onclick=()=>{kind=k==='itemsTab'?'items':'backgrounds';if(kind==='backgrounds'){pending=null;ghost=null;schedule();}drawPalette(true)};
  for(const k of ['family','groupFilter'])$(k).onchange=()=>drawPalette(true);
  $('search').oninput=()=>drawPalette(true);$('assetPrev').onclick=()=>{assetPage--;drawPalette()};$('assetNext').onclick=()=>{assetPage++;drawPalette()};
  $('layerTab').onclick=()=>{inspector='layer';renderPanel()};$('boxTab').onclick=()=>{inspector='box';renderPanel()};
  $('new').onclick=()=>{if(level.items.length&&!confirm('Mở màn mới? Lưu JSON trước nếu cần giữ bản hiện tại.'))return;batch=null;openLevel(newLevel());drawPalette();say('Chọn ảnh nền và đồ vật ở cột bên trái.');};
  $('title').onchange=()=>{const name=$('title').value.trim();if(name)patch(()=>{level.name=name;level.key=slug(name)});$('title').value=level.name;};
  $('undo').onclick=()=>rewind(true);$('redo').onclick=()=>rewind(false);
  $('center').onclick=()=>{view={zoom:1,dx:0,dy:0};schedule()};
  $('placeCenter').onclick=()=>{if(pending&&!game){ghost=null;place({x:0,y:0},pending,level);}};
  $('grid').onclick=()=>{showGrid=!showGrid;$('grid').classList.toggle('active',showGrid);$('grid').setAttribute('aria-pressed',showGrid);schedule()};
  $('layerBack').onclick=()=>arrange(-1);$('layerFront').onclick=()=>arrange(1);$('delete').onclick=removeItem;$('duplicate').onclick=duplicate;
  $('fitItem').onclick=()=>{if(item())resetSize([item()]);};$('fitAll').onclick=()=>{if(level)resetSize([...level.items]);};
  for(const k of ['x','y','angle','scaleX','scaleY'])$(k).onchange=()=>{
    const it=item(),n=+$(k).value,scale=k.startsWith('scale');if(!it)return;
    if($(k).value!==''&&Number.isFinite(n)&&Math.abs(n)<=(scale?1000:1e7)&&(!scale||Math.abs(n)>=.0001))patch(()=>it[k]=ROUND(n) || (scale?n:0));
    $(k).value=it[k];
  };
  $('itemGroup').onchange=()=>{const it=item();if(!it)return;const g=+$('itemGroup').value;patch(()=>{it.group=g;it.targetType=level.boxes.find(o=>o.group===g)?.targetType??level.items.find(i=>i!==it&&i.group===g)?.targetType??g;});};
  $('rule').onchange=()=>patch(()=>level.rule=$('rule').value);
  $('addBox').onclick=()=>{const group=+$('groupOrder').value;patch(()=>level.boxes.push({group,targetType:level.items.find(i=>i.group===group)?.targetType??group,label:label(group),count:1}));};
  $('fillBoxes').onclick=()=>{if(level.boxes.length&&!confirm('Tạo lại toàn bộ hàng đợi hộp từ số đồ đang có?'))return;patch(()=>{
    const totals=new Map();for(const i of sorted(level.items).reverse()){
      if(!totals.has(i.group))totals.set(i.group,{group:i.group,targetType:i.targetType,label:level.boxes.find(o=>o.group===i.group)?.label||label(i.group),count:0});totals.get(i.group).count++;
    }
    level.boxes=[...totals.values()];
  });};
  $('play').onclick=startPlay;$('exitPlay').onclick=startPlay;$('restart').onclick=restart;
  $('library').onclick=()=>{$('importStatus').textContent='';$('loadDialog').showModal()};
  $('loadOne').onclick=()=>source('unity',$('unityLevel').value);$('allUnity').onclick=()=>source('unity');$('allRoom').onclick=()=>source('roomsort');$('allHappy').onclick=()=>source('happy');
  for(const k of ['files','folder'])$(k).onchange=()=>{importFiles($(k).files);$(k).value='';};
  $('drop').ondragover=e=>{e.preventDefault();$('drop').classList.add('over')};$('drop').ondragleave=()=>$('drop').classList.remove('over');
  $('drop').ondrop=e=>{e.preventDefault();$('drop').classList.remove('over');importFiles(e.dataTransfer.files)};
  $('batchLevel').onchange=()=>{syncBatch();const p=+$('batchLevel').value;openLevel(clone(batch.levels[p]),p);drawPalette();say(`Đang sửa màn ${p+1}/${batch.levels.length}.`);};
  $('savePack').onclick=()=>{syncBatch();download('tidy-level-pack.json',batch)};
  $('download').onclick=()=>download(level.key+'.tidy.json',level);
  $('showReport').onclick=openReport;
  $('downloadReport').onclick=()=>download('import-report.json',{total:batch.levels.length,rejected:batch.rejected,warnings:batch.levels.filter(l=>l.origin?.warnings?.length).map(l=>({key:l.key,warnings:l.origin.warnings}))});
  $('unity').onclick=()=>{
    if(!check(level).ok){inspector='box';renderPanel();say('Cần sửa số đồ và số chỗ trong hộp trước khi xuất Unity.');return;}
    $('unityTarget').textContent=`Project đích: ${catalog.unity}. “Thêm màn” tạo bản mới trong danh sách Levels.`;
    $('unityStatus').textContent='';$('unityDialog').showModal();
  };
  $('downloadUnity').onclick=()=>exportUnity(false);$('installUnity').onclick=()=>exportUnity(true);
  document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>$(b.dataset.close).close());
  document.addEventListener('keyup',e=>{if(e.code==='Space')space=false;});window.addEventListener('blur',()=>space=false);
  document.addEventListener('keydown',e=>{
    if(document.querySelector('dialog[open]'))return;
    if(e.key==='Escape'&&pending){pending=null;ghost=null;renderPlacement();schedule();say('Đã dừng đặt đồ. Bấm một món trên nền để di chuyển.');}
    if(e.target.matches('input,select,textarea'))return;
    if(e.code==='Space'&&e.target===document.body){space=true;e.preventDefault();}
    if(!level||game)return;
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){rewind(!e.shiftKey);e.preventDefault();}
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='y'){rewind(false);e.preventDefault();}
    if(e.key==='Delete'&&item()){removeItem();e.preventDefault();}
  });
}
async function exportUnity(install){
  $('installUnity').disabled=$('downloadUnity').disabled=true;$('unityStatus').textContent='Đang chuyển cấu trúc và kiểm tra ảnh…';
  try{
    const data=await api(install?'/api/install':'/api/export',{level});
    if(install){catalog.library.push(data);setLibrary(catalog.library);$('unityStatus').textContent=`Đã thêm ${data.label}. Trong Unity, dừng rồi bấm Play lại, mở Levels → ${data.source==='Happy'?'Happy reference':'RoomSort / Tidy Room'}. Màn mới nằm ở cuối.`;}
    else{download(level.key+'.unity.json',data);$('unityStatus').textContent='Đã xuất JSON LevelData.';}
  }catch(e){$('unityStatus').textContent=e.message;}finally{$('installUnity').disabled=$('downloadUnity').disabled=false;}
}

try{
  catalog=await api('/api/catalog');assetLookup=new Map(catalog.items.map(a=>[a.path,a]));groupNames=new Map(catalog.items.filter(a=>a.group!==null).map(a=>[a.group,a.label]));groupNames.set(0,'Chưa gán nhóm');
  $('assetTotal').textContent=`${catalog.items.length.toLocaleString('vi')} sprite · ${catalog.backgrounds.length} nền`;
  setLibrary(catalog.library);$('allRoom').disabled=!catalog.sources.roomsort;$('allHappy').disabled=!catalog.sources.happy;
  bind();const draft=await readDraft().catch(()=>null);
  if(draft?.level?.schema==='tidy-level-tool/1'&&catalog.backgrounds.some(b=>b.path===draft.level.background.asset)){
    batch=draft.batch;openLevel(draft.level,draft.batchPos);say('Đã mở bản nháp lưu trên trình duyệt này.');
  }else{openLevel(newLevel());say('Chọn ảnh hoặc đồ trong thư viện Unity. Chuột phải để kéo nền · lăn để zoom.');}
  drawPalette();
}catch(e){say(`Không mở được tool: ${e.message}`);}
