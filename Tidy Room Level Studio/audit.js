import fs from 'node:fs/promises';
import path from 'node:path';
import {Game} from './core/game.js';
import {hash,signature} from './studio.js';
import {fileURLToPath} from 'node:url';

const root=fileURLToPath(new URL('./',import.meta.url));
const read=p=>fs.readFile(path.resolve(root,p),'utf8').then(JSON.parse);
const {items}=await read('data/art.json');const ref=await read('data/references.json');
const name=process.argv[2]??'2026-11-20T09-25-05-444Z-seed42';
const base=path.join('batches',name),pack=await read(path.join(base,'pack.json')),report=await read(path.join(base,'validation.json'));
if(hash(pack)!==report.packHash)throw Error('Pack does not match validation report');
const pct=(a,b)=>Math.round(100*a/b);
function play(level,shapes,policy,path=null,strict=false){
 const g=new Game(level,shapes);let peak=0,waits=0,taps=0,forced=0;const coords=[];
 const remaining=new Set(g.items),free=new Set(),under=new Map();if(!path){
  g.items.forEach((o,i)=>{if(!g.isCovered(i))free.add(o);for(const p of o.coverCandidates??[]){if(!under.has(p))under.set(p,[]);under.get(p).push(o);}});
 }
 // Full visibility heuristics, not human agents: choose a direct match first; if blocked, choose a loose filler.
 const tray=()=>g.buffer.filter(x=>x.item).length;
 while(g.state==='playing'&&taps<level.content.length){
  if(strict&&tray()>=5)return{win:false,taps,peak,waits,forced,reason:'strict-capacity'};
  if(path){const uid=path[taps],item=g.items.find(x=>x.uid===uid);if(!item)return{win:false,reason:'unknown UID',taps};
   const {minX,maxX,minY,maxY}=item.aabb;let dest=null;
   for(const n of [1,5,11]){for(let i=0;i<n*n;i++){const x=minX+(maxX-minX)*((i%n)+.5)/n,y=minY+(maxY-minY)*(Math.floor(i/n)+.5)/n;if(g.pickAt(x,y)===uid){dest=[x,y];break}}if(dest)break}
   if(!dest)return{win:false,reason:'no selectable point found',taps,uid};
   coords.push(dest.map(v=>+v.toFixed(5)));g.tapAt(...dest);
  }else{
   const a=[...free].sort((a,b)=>a.uid-b.uid),open=g.orders.filter(x=>x.open&&x.type>=0),matches=new Set(open.map(o=>o.type)),accessible=a.filter(x=>matches.has(x.type));if(!a.length)return{win:false,taps,peak,waits,forced,reason:'no candidate'};
   if(!accessible.length)forced++;
   const choices=accessible.length?accessible:a;
   const impact=x=>(under.get(x)??[]).reduce((n,it)=>n+(remaining.has(it)&&matches.has(it.type)&&it.coverCandidates.filter(q=>remaining.has(q)).length===1?1:0),0);
   let x;
   if(policy==='top-first')x=choices.at(-1);
   else if(accessible.length)x=choices.map(it=>({it,s:Math.max(...open.filter(o=>o.type===it.type).map(o=>o.count-o.total))*4+impact(it)})).sort((a,b)=>b.s-a.s||b.it.uid-a.it.uid)[0].it;
   else x=choices.map(it=>({it,s:impact(it)*8-Math.max(0,g.queue.findIndex((q,i)=>i>=g.next&&q.type===it.type)-g.next)})).sort((a,b)=>b.s-a.s||b.it.uid-a.it.uid)[0].it;
   g.tapItem(x.uid);remaining.delete(x);free.delete(x);
   for(const it of under.get(x)??[])if(remaining.has(it)&&!free.has(it)&&!g.isCovered(g.items.indexOf(it)))free.add(it);
  }
  waits+=g.events.some(e=>e.t==='toBuffer')?1:0;g.events=[];peak=Math.max(peak,tray());taps++;
 }
 return {win:g.state==='win',taps,waits,peak,forced,...(path?{coords}:{}),reason:g.state};
}
const result=[];
for(const x of pack.records){
 const original=ref.levels.find(r=>r.level===x.level.level),n=x.level.content.length;
 const w=play(x.level,items,null,x.path,pack.strict);if(!w.win||w.taps!==n)throw Error('Pointer verification failed '+JSON.stringify({level:x.level.level,...w}));
 if(signature(x.level,items)!==x.fingerprint)throw Error('Structural fingerprint does not match');
 const heuristics={};for(const policy of ['top-first','prioritize-unblock'])heuristics[policy]={roomsort:play(original,ref.shapes,policy),generated:play(x.level,items,policy)};
 result.push({level:x.level.level,path:w.coords,peak:w.peak,heuristics});console.log('Checked',x.level.level,'pointer win, peak',w.peak);
}
const summary=Object.fromEntries(['top-first','prioritize-unblock'].map(k=>[k,Object.fromEntries(['roomsort','generated'].map(x=>[x,{wins:result.filter(r=>r.heuristics[k][x].win).length,total:result.length}]))]));
await fs.writeFile(path.resolve(root,base,'pointer-audit.json'),JSON.stringify({packHash:report.packHash,strict:pack.strict,summary,notes:'Policies see full candidate and blocker geometry; they are diagnostic-only, and use default RoomSort fail logic for apples-to-apples comparisons.',levels:result},null,2));
console.log(JSON.stringify(summary));
