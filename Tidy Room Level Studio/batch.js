import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {hash,generateOne,replay,verifyTemplate} from './studio.js';

const root=fileURLToPath(new URL('./',import.meta.url));
function read(p){return fs.readFile(path.join(root,p),'utf8').then(JSON.parse)}
export async function load(){const [art,model]=await Promise.all([read('data/art.json'),read('data/model.json')]);return {art,model}}
export async function runBatch(opts={},onProgress=()=>{},cancel=()=>false){
 const {art,model}=await load(), seed=Number(opts.seed??42), start=Number(opts.start??1), count=Number(opts.count??10), strict=opts.strict!==false;
 if(!Number.isSafeInteger(seed)||!Number.isInteger(start)||!Number.isInteger(count)||start<1||count<1||count>130||start+count-1>model.targets.length)throw Error(`Chọn 1–${model.targets.length}, không vượt quá mốc cuối; seed phải nguyên.`);
 if(opts.room&&!Object.hasOwn(art.rooms,opts.room))throw Error('Không tìm thấy template.');
 if(opts.template){if(!opts.room)throw Error('Chọn nền cụ thể để dùng template chỉnh sửa.');const r=art.rooms[opts.room];art.rooms[opts.room]=verifyTemplate({...r,zones:opts.template.zones,anchors:opts.template.anchors},art);}
 const batchName=new Date().toISOString().replace(/[:.]/g,'-')+`-seed${seed}`;
 const output=path.join(root,'batches',batchName);await fs.mkdir(output,{recursive:false});
 const sourceSet=new Set(model.fingerprints),oldSet=new Set(); const accepted=[],blocked=[],rejections={};
 // Past complete runs automatically serve as exclusions. Incomplete partials remain separate.
 if(opts.exclude!==false)for(const dir of await fs.readdir(path.join(root,'batches'),{withFileTypes:true}))if(dir.isDirectory()){
  try{const q=JSON.parse(await fs.readFile(path.join(root,'batches',dir.name,'pack.json'),'utf8'));for(const v of q.records??[])oldSet.add(v.fingerprint)}catch(e){if(e.code!=='ENOENT')throw e;}
 }
 const source=hash(model.targets), inputs={source:model.sourceHash,models:hash(model),art:hash(art),sourceProfiles:source,adapter:model.adapterHash,core:model.rulesHash,geometry:model.geometryHash,rules:model.rulesConfigHash};
 const actual={adapter:await fs.readFile(path.join(root,'studio.js'),'utf8'),core:await fs.readFile(path.join(root,'core/game.js'),'utf8'),geometry:await fs.readFile(path.join(root,'core/geometry.js'),'utf8'),rules:await fs.readFile(path.join(root,'core/rules.js'),'utf8')};
 for(const [key,value] of Object.entries(actual))if(hash(value)!==inputs[key])throw Error(`${key} changed; retrain before generation`);
 const prev=new Set([...sourceSet,...oldSet]);let stopped=false;
 const pack=()=>({schema:'tidy-room-level-studio/v1',status:stopped?'cancelled':accepted.length===count?'complete':'incomplete',seed,start,count,strict,inputs,records:accepted,blocked,rejections});
 const save=async(p,data)=>{const tmp=path.join(output,p+'.next');await fs.writeFile(tmp,JSON.stringify(data,null,2));await fs.rename(tmp,path.join(output,p))};
 const progress=p=>onProgress({...p,batchName,accepted:accepted.length,count});
 for(let i=0;i<count;i++){
  if(cancel()){stopped=true;break;}
  const target=model.targets[start+i-1];progress({phase:'working',level:target.level});
  const stepSeed=((seed>>>0)^Math.imul(target.level,2654435761))>>>0;
  const {best,rejection}=generateOne(target,art,model,stepSeed,prev,{room:opts.room,strict,attempts:opts.attempts??26});
  for(const [k,v] of Object.entries(rejection))rejections[k]=(rejections[k]??0)+v;
  if(best){
   const result=replay(best.level,art.items,best.path,{strict});if(!result.ok)throw Error('Final replay failed');
   prev.add(best.fingerprint);accepted.push({...best,target:{...target,boxSizes:undefined,typePattern:undefined}});
  }else blocked.push({level:target.level,rejection});
  await save('checkpoint.json',pack());
  progress({phase:'checked',level:target.level,passed:!!best,features:best?.features});
  await new Promise(r=>setImmediate(r));
 }
 const final=pack();await save(final.status==='complete'?'pack.json':'partial.json',final);
 const levelRows=accepted.map(x=>({position:x.level.level,sourceOdds:x.target.odds,estimateOdds:x.estimateOdds,items:x.features.items,boxes:x.features.boxes,groups:x.features.groups,freeRef:x.target.free,freeStudio:x.features.free,contactsRef:x.target.contacts,contactsStudio:x.features.contacts,peak:x.proof.peak,waits:x.proof.waits,signature:x.fingerprint}));
 const cols=['position','sourceOdds','estimateOdds','items','boxes','groups','freeRef','freeStudio','contactsRef','contactsStudio','peak','waits','signature'];
 await fs.writeFile(path.join(output,'progression.csv'),[cols.join(','),...levelRows.map(x=>cols.map(c=>x[c]??'').join(','))].join('\n')+'\n');
 if(final.status==='complete'){
  await save('levels.json',{schema:'tidy-room-layout/v1',coordinateSpace:'pixels relative to background center; x right; y up; angle CCW; content bottom to top',levels:accepted.map(x=>x.level)});
 }
 await save('validation.json',{status:final.status,requested:count,accepted:accepted.length,sourceStructuralNovelty:sourceSet.size,priorStructuralNovelty:oldSet.size,rule:strict?'RoomSort + reject witness reaching 5 filled slots':'RoomSort standard',noBoosters:true,replay:'UID and actual RoomSort hit-test coordinates',inputs,packHash:hash(final),rejections,blocked,levels:levelRows});
 progress({phase:'done',status:final.status,blocked,output});return {status:final.status,batchName,accepted:accepted.length,blocked,output};
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const args=Object.fromEntries(process.argv.slice(2).filter(x=>x.startsWith('--')).map(x=>x.slice(2).split('=')));
 const result=await runBatch({...args,strict:args.strict!=='false',exclude:args.exclude!=='false',attempts:args.attempts?Number(args.attempts):undefined},p=>console.log(JSON.stringify(p)));
 if(result.status!=='complete')process.exitCode=2;
}
