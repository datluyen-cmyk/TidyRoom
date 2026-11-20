import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {Game} from '../core/game.js';
import * as G from '../core/geometry.js';
import {COVER_CONTACT_MIN, COVER_BLOCK_MIN, COVER_EXACT_LIMIT} from '../core/rules.js';

const project = path.dirname(fileURLToPath(import.meta.url));
const studio = path.dirname(project);
const source = process.argv[2] ?? path.join(studio, 'batches', '2026-11-20T09-39-07-460Z-seed42', 'pack.json');
const art = JSON.parse(fs.readFileSync(path.join(studio, 'data', 'art.json'), 'utf8'));
const pack = JSON.parse(fs.readFileSync(source, 'utf8'));
if (pack.schema !== 'tidy-room-level-studio/v1' || !pack.records?.length) throw Error('Choose a Studio pack.json with levels.');
const output = path.join(project, 'Assets', 'Resources', 'TidyPreview');
fs.mkdirSync(path.join(output, 'Artwork'), {recursive:true});
const images = new Map();
const vec = ([x,y]) => ({x,y});
function addImage(asset, key) {
  const src = path.join(studio, asset.src);
  if (!fs.existsSync(src)) throw Error(`Missing art: ${src}`);
  images.set(key, src);
  return key;
}

function coverData(it, later) {
  const covers = later.filter(b => G.aabbIntersects(it.aabb,b.aabb) && G.polygonsTouch(it.poly,b.poly) && G.overlapRatio(it.poly,b.poly) >= COVER_CONTACT_MIN);
  if (!covers.length) return {covers:[], pairs:[], sampleCount:0};
  // RoomSort computes overlap exactly for up to two covering silhouettes, then samples the union.
  const pairs = [];
  for(let a=0;a<covers.length;a++) for(let b=a+1;b<covers.length;b++) {
    if(G.unionOverlapRatio(it.poly,[covers[a].poly,covers[b].poly],COVER_EXACT_LIMIT)>=COVER_BLOCK_MIN) pairs.push({x:covers[a].uid,y:covers[b].uid});
  }
  const points = [];
  if(covers.length>2) {
    const {minX,minY,maxX,maxY} = G.bounds(it.poly);
    for(let i=0;i<64;i++) for(let j=0;j<64;j++) {
      const p=[minX+(i+.5)*(maxX-minX)/64,minY+(j+.5)*(maxY-minY)/64];
      if(G.pointInPolygon(p,it.poly)) points.push(p);
    }
  }
  return {sampleCount:points.length,pairs,covers:covers.map(b=>{
    const bits=Buffer.alloc(Math.ceil(points.length/8));
    points.forEach((p,i)=>{if(G.pointInPolygon(p,b.poly))bits[i>>3]|=1<<(i&7);});
    return {uid:b.uid,alone:G.unionOverlapRatio(it.poly,[b.poly],COVER_EXACT_LIMIT)>=COVER_BLOCK_MIN,bits:bits.toString('base64')};
  })};
}

const levels=pack.records.map(({level,points,path:uids,proof})=>{
  const room=art.rooms[level.bg];
  if (!room || level.width!==room.w || level.height!==room.h || points?.length!==level.content.length) throw Error(`Unsupported room or missing pointer proof: ${level.name}`);
  const game=new Game(level,art.items);
  const representatives=new Map();
  const items=game.items.map((it,index)=>{
    const sprite=art.items[it.id];
    if(sprite.alphaMask)throw Error(`This preview exporter expects the Studio polygon shapes. Unexpected mask: ${it.id}`);
    const image=addImage(sprite,it.id);
    if(!representatives.has(it.type))representatives.set(it.type,image);
    return {image,type:it.type,x:it.x,y:it.y,w:sprite.w*it.scaleX,h:sprite.h*it.scaleY,angle:it.angle,poly:it.poly.map(vec),...coverData(it,game.items.slice(index+1))};
  });
  console.log(`Prepared level ${level.level}: ${items.length} objects`);
  return {number:level.level,label:level.name,room:addImage(room,level.bg),w:room.w,h:room.h,items,
    order:level.order.map(({type,count})=>({type,count,label:art.types[type]??`Nhóm ${type}`,image:representatives.get(type)})),
    proof:points.map(vec),uids,peak:proof.peak};
});

const converter=`import json, pathlib, sys\nfrom PIL import Image\nfor dest, src in json.load(sys.stdin):\n    dest = pathlib.Path(dest)\n    if dest.exists() and dest.stat().st_mtime >= pathlib.Path(src).stat().st_mtime:\n        continue\n    with Image.open(src) as im:\n        im.convert('RGBA').save(dest, compress_level=5)\n`;
const converted=spawnSync(process.env.TIDY_PREVIEW_PYTHON || 'python',['-X','utf8','-c',converter],{
  input:JSON.stringify([...images].map(([key,src])=>[path.join(output,'Artwork',`${key}.png`),src])),encoding:'utf8',windowsHide:true,
});
if(converted.error || converted.status!==0) throw Error(`PNG conversion needs Python with Pillow. ${converted.error??converted.stderr}`);
const file=path.join(output,'Levels.json');
fs.writeFileSync(file+'.tmp',JSON.stringify({strict:pack.strict===true,coverThreshold:COVER_BLOCK_MIN,levels}));
fs.renameSync(file+'.tmp',file);
console.log(`Ready: ${levels.length} level(s), ${images.size} textures.`);
