// Uses the source game's geometry functions, including exact overlap for 1-2 covers.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const project=new URL('../',import.meta.url);
const root=process.argv[2]||'D:/APK Works/RoomSort/analysis';
const {Game}=await import(pathToFileURL(root+'/www/game/src/core/game.js'));
const G=await import(pathToFileURL(root+'/www/game/src/core/geometry.js'));
const source=JSON.parse(fs.readFileSync(new URL('Tools/Source/room.json',project),'utf8'));
let maxWeak=0,count=0;
for(const level of source.levels) {
 const g=new Game(level,source.shapes);
 const file=new URL(`Assets/StreamingAssets/TidyRoom/Levels/${level.key}.json`,project);
 const output=JSON.parse(fs.readFileSync(file,'utf8'));
 for(let i=0;i<g.items.length;i++) {
  const me=g.items[i];g.isCovered(i);
  const covers=me.coverCandidates||[];
  const ratios=covers.map(c=>G.overlapRatio(me.poly,c.poly));
  const weak=covers.filter((_,j)=>ratios[j]<.045);maxWeak=Math.max(maxWeak,weak.length);
  const pairs=[];
  for(let a=0;a<covers.length;a++)for(let b=a+1;b<covers.length;b++)
   if(ratios[a]<.045&&ratios[b]<.045&&ratios[a]+ratios[b]>=.045)
    pairs.push({a:covers[a].uid,b:covers[b].uid,ratio:G.unionOverlapRatio(me.poly,[covers[a].poly,covers[b].poly],2)});
  let points=[];
  const bounds=G.bounds(me.poly);
  for(let x=0;x<64;x++)for(let y=0;y<64;y++) {
   const p=[bounds.minX+(x+.5)*(bounds.maxX-bounds.minX)/64,bounds.minY+(y+.5)*(bounds.maxY-bounds.minY)/64];
   if(G.pointInPolygon(p,me.poly))points.push(p);
  }
  output.content[i].reference={samples:points.length,pairs,covers:covers.map((c,j)=>{
   const bits=new Uint32Array(Math.ceil(points.length/32));
   points.forEach((p,k)=>{if(G.pointInPolygon(p,c.poly))bits[k>>>5]|=1<<(k&31)});
   return {uid:c.uid,ratio:ratios[j],bits:Array.from(bits)};
  })};
 }
 fs.writeFileSync(file,JSON.stringify(output));count++;
 if(count%20===0)console.log(`Baked ${count}/${source.levels.length}`);
}
console.log(JSON.stringify({boards:count,maxWeak}));
