import fs from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const root='D:/APK Works/RoomSort/analysis';
const mod=async p=>import(pathToFileURL(`${root}/www/game/src/${p}`).href);
const payload=JSON.parse(await fs.readFile(`${root}/room-content-expanded.json`,'utf8'));
const happy=JSON.parse(await fs.readFile(`${root}/happy-levels.json`,'utf8'));
const {Game}=await mod('core/game.js');
const {selectExperimentLevel}=await mod('services/workshop-experiment.js');
const {checkOrder,checkFeel,applyDeal}=await mod('services/deal-variant.js');
const {LEVEL_ODDS}=await mod('data/level-odds.js');
const shapes=payload.expanded.catalog.items;
const summary=(l,typeOf)=>{const q=l.order.map(x=>x.type),types=new Set(q),counts={};for(const x of l.order)counts[x.count]=(counts[x.count]??0)+1;const gaps=[];for(let i=0;i<q.length;i++){const j=q.lastIndexOf(q[i],i-1);if(i&&j>=0&&j<i)gaps.push(i-j);}return{level:l.level??l._file,name:l.name??l.levelName,items:l.content.length,uniqueAssets:new Set(l.content.map(x=>x.id)).size,types:types.size,boxes:l.order.length,boxSizeCounts:counts,repeatBoxes:q.length-types.size,repeatGapMin:gaps.length?Math.min(...gaps):null,repeatGapAvg:gaps.length?gaps.reduce((a,b)=>a+b,0)/gaps.length:null,orderMatchesItems:(()=>{const a={},b={};for(const x of l.content){const t=typeOf(x.id);a[t]=(a[t]??0)+1;}for(const o of l.order)b[o.type]=(b[o.type]??0)+o.count;return JSON.stringify(Object.entries(a).sort())===JSON.stringify(Object.entries(b).sort())})()};};
const happyCatalog=JSON.parse(await fs.readFile('D:/APK Works/HappyTidyRoom/analysis/mono/resources.assets_7861.json','utf8'));
const happyType=Object.fromEntries(happyCatalog.items.map(x=>[x.id,x.subGroup]));
const happyStats=happy.map(l=>summary(l,id=>happyType[id]));
const roomStats=payload.base.levels.map(l=>summary(l,id=>parseInt(id,10)));
const rooms=[];
function addRoom(key,l){const g=new Game(l,shapes),free=g.items.map((it,i)=>!g.isCovered(i)?it:null).filter(Boolean),wanted=new Set(g.orders.filter(o=>o.open).map(o=>o.type));rooms.push({key,...summary(l,id=>parseInt(id,10)),freeAtStart:free.length,directAtStart:free.filter(x=>wanted.has(x.type)).length,orderCheck:checkOrder(l,l.order),feelCheck:checkFeel(l.order)});}
for(const l of payload.base.levels.slice(0,10))addRoom(`baseline_${l.level}`,l);
for(const [key,c]of Object.entries(payload.rooms)){
 if(c.level&&Array.isArray(c.level.content))addRoom(key,c.level);
}
const proofs=[];
for(const [variant,v]of Object.entries(payload.variants))for(const [lev,p]of Object.entries(v.proofs??{})){
 const l=applyDeal(payload.base.levels.find(l=>l.level===Number(lev)),variant);
 const g=new Game(l,shapes);let peak=0,blocked=0;
 for(let i=2;i<p.boxes;i++)g.unlockOrderSlot();for(let i=5;i<p.slots;i++)g.unlockBufferSlot();
 for(const uid of p.path){g.events=[];g.tapItem(uid);peak=Math.max(peak,g.buffer.filter(s=>s.item).length);blocked+=g.events.filter(e=>e.t==='blocked').length;}
 proofs.push({variant,level:Number(lev),state:g.state,items:l.content.length,boxes:l.order.length,slots:p.slots,orderSlots:p.boxes,pathLength:p.path.length,peakBuffer:peak,blocked});
}
const simple={};for(const t of [1,2,3])for(let i=0;i<5;i++)simple[`${t}-${i}`]={w:10,h:10,poly:[[-5,-5],[5,-5],[5,5],[-5,5]]};
const l={order:[{type:1,count:1},{type:2,count:1},{type:3,count:5}],content:[{id:'1-0',x:0,y:0,scaleX:1,scaleY:1,angle:0},{id:'2-0',x:20,y:0,scaleX:1,scaleY:1,angle:0},...Array.from({length:5},(_,i)=>({id:`3-${i}`,x:40+i*20,y:0,scaleX:1,scaleY:1,angle:0}))]};
const g=new Game(l,simple);for(let i=2;i<7;i++)g.tapItem(i);
const fullBufferState=g.state,fullBufferUsed=g.buffer.filter(s=>s.item).length;
g.tapItem(0);g.tapItem(1);
const mechanicsProbe={fullBufferState,fullBufferUsed,finalState:g.state};
const data={roomStats,happyStats,rooms,proofs,mechanicsProbe,levelOdds:LEVEL_ODDS};
await fs.writeFile(`${root}/design-comparison.json`,JSON.stringify(data,null,2));
console.log(JSON.stringify({roomFirst10:roomStats.slice(0,10),happyFirst:happyStats.slice(0,10),roomExperiments:rooms.filter(x=>!x.key.startsWith('baseline')),proofs,mechanicsProbe},null,2));
