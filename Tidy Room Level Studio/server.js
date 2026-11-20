import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Worker,isMainThread,parentPort,workerData} from 'node:worker_threads';
import {runBatch} from './batch.js';

const base=fileURLToPath(new URL('./',import.meta.url));
if(!isMainThread){
 try{const flag=new Int32Array(workerData.cancel);const result=await runBatch(workerData.options,p=>parentPort.postMessage({progress:p}),()=>Atomics.load(flag,0)>0);parentPort.postMessage({result});}
 catch(e){parentPort.postMessage({error:e.message})}
}else{
 let job=null;
 const json=(res,body,code=200)=>{res.writeHead(code,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}).end(JSON.stringify(body));};
 async function body(req){const chunks=[];let n=0;for await(const b of req){n+=b.length;if(n>160000)throw Error('Yêu cầu quá dài.');chunks.push(b)}return JSON.parse(Buffer.concat(chunks).toString()||'{}')}
 const server=http.createServer(async(req,res)=>{
  try{
   const url=new URL(req.url,'http://localhost'),p=decodeURIComponent(url.pathname);
   if(req.method==='POST'){
    if(req.headers.origin&&!['http://127.0.0.1:'+server.address().port,'http://localhost:'+server.address().port].includes(req.headers.origin))return json(res,{error:'Origin không hợp lệ.'},403);
    if(p==='/api/start'){
     if(job?.active)return json(res,{error:'Đang có lượt sinh level.'},409);
     const payload=await body(req);if(job?.active)return json(res,{error:'Đang có lượt sinh level.'},409);
     const flag=new SharedArrayBuffer(4), j={active:true,log:[],flag,result:null,error:null};job=j;
     const w=new Worker(new URL(import.meta.url),{workerData:{options:{seed:payload.seed,start:payload.start,count:payload.count,strict:payload.strict!==false,room:payload.room||undefined,template:payload.template,exclude:payload.exclude!==false},cancel:flag}});
     w.on('message',m=>{if(m.progress)j.log.push(m.progress);if(m.result){j.result=m.result;j.active=false;}if(m.error){j.active=false;j.error=m.error;}});
     w.on('error',e=>{j.active=false;j.error=e.message;});w.on('exit',code=>{if(j.active){j.active=false;j.error=`Tiến trình dừng (mã ${code}).`;}});
     return json(res,{started:true});
    }
    if(p==='/api/stop'){if(job?.active)Atomics.store(new Int32Array(job.flag),0,1);return json(res,{stopping:!!job?.active});}
    return json(res,{error:'Không có đường dẫn.'},404);
   }
   if(req.method!=='GET')return json(res,{error:'Không hỗ trợ.'},405);
   if(p==='/api/status')return json(res,job?{active:job.active,log:job.log,result:job.result,error:job.error}:{active:false,log:[]});
   if(p==='/api/batches'){
    const a=await fs.readdir(path.join(base,'batches'),{withFileTypes:true});return json(res,a.filter(x=>x.isDirectory()&&/^\d{4}-[0-9TZ-]+-seed-?\d+$/.test(x.name)).map(x=>x.name).sort().reverse());
   }
   const file=p==='/'?'index.html':p.slice(1);
   if(!/^(index\.html|ui\.js|core\/(game|rules|geometry)\.js|data\/(art|model)\.json|art\/[\w-]+\.webp|batches\/\d{4}-[0-9TZ-]+-seed-?\d+\/(pack|partial|checkpoint|levels|validation)\.json|batches\/\d{4}-[0-9TZ-]+-seed-?\d+\/progression\.csv)$/.test(file))return json(res,{error:'Không có tệp.'},404);
   const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.webp':'image/webp','.csv':'text/csv; charset=utf-8'};
   const data=await fs.readFile(path.join(base,file));res.writeHead(200,{'Content-Type':mime[path.extname(file)],'Cache-Control':file.startsWith('art/')?'public, max-age=3600':'no-store'}).end(data);
  }catch(e){json(res,{error:e.code==='ENOENT'?'Không có tệp.':e.message},e.code==='ENOENT'?404:400);}
 });
 const arg=process.argv.find(x=>x.startsWith('--port='));
 server.listen(arg?Number(arg.slice(7)):37846,'127.0.0.1',()=>{const url=`http://127.0.0.1:${server.address().port}`;console.log(url);});
}
