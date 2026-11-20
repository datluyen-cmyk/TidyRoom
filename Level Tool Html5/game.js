export const sorted = items => [...items].sort((a,b)=>a.layer-b.layer);
export const ROUND = n=>Math.round(n*1000)/1000;

function geometry(item, mask){
  const a=item.angle*Math.PI/180, c=Math.cos(a), s=Math.sin(a);
  const halfW=Math.abs(item.width*item.scaleX)/2, halfH=Math.abs(item.height*item.scaleY)/2;
  return {item,mask,c,s,hx:Math.abs(c)*halfW+Math.abs(s)*halfH,hy:Math.abs(s)*halfW+Math.abs(c)*halfH};
}
function hit(g,x,y){
  const {item:i,mask:m,c,s}=g,dx=x-i.x,dy=y-i.y;
  const u=(dx*c+dy*s)/(i.scaleX*i.width)+.5, v=.5-(-dx*s+dy*c)/(i.scaleY*i.height);
  if(u<0||u>=1||v<0||v>=1)return false;
  return !m||!!m.alpha[Math.floor(v*m.maskH)*m.maskW+Math.floor(u*m.maskW)];
}
export function itemAt(items,x,y,masks,visible=()=>true){
  for(let i=items.length-1;i>=0;i--){const it=items[i];if(visible(it)&&hit(geometry(it,masks.get(it.asset)),x,y))return it;}
  return null;
}

export function check(level){
  const rows=new Map(); function row(k){if(!rows.has(k))rows.set(k,{group:k,have:0,want:0});return rows.get(k);}
  for(const it of level.items)row(it.group).have++;
  for(const b of level.boxes)row(b.group).want+=b.count;
  const deltas=[...rows.values()].filter(x=>x.have!==x.want);
  return {ok:level.items.length>0&&!deltas.length,deltas};
}

// Mirrors TidyModel's image collision and box / tray settlement.
export class Playtest{
  constructor(level,masks){
    this.level=level;this.items=sorted(level.items);this.geom=this.items.map(i=>geometry(i,masks.get(i.asset)));
    if(this.geom.some(g=>!g.mask))throw Error('Chưa đủ viền ảnh để playtest.');
    this.room=new Set(this.items.map((_,i)=>i));this.tray=[];this.cache=new Map();this.boxes=[{index:-1,count:0},{index:-1,count:0}];
    this.next=0;this.moves=0;this.peak=0;this.delivered=0;this.state='playing';this.log=[];
    this.boxes.forEach(b=>this.assign(b));
  }
  assign(b){b.index=this.next<this.level.boxes.length?this.next++:-1;b.count=0;}
  order(b){return this.level.boxes[b.index];}
  box(group){let best=-1;this.boxes.forEach((b,i)=>{if(this.order(b)?.group===group&&(best<0||b.count>this.boxes[best].count))best=i});return best;}
  coverData(uid){
    if(this.cache.has(uid))return this.cache.get(uid);
    const g=this.geom[uid],m=g.mask,it=g.item,points=[],covers=[];
    for(let y=0;y<m.maskH;y++)for(let x=0;x<m.maskW;x++)if(m.alpha[y*m.maskW+x]){
      const u=((x+.5)/m.maskW-.5)*it.width*it.scaleX,v=(.5-(y+.5)/m.maskH)*it.height*it.scaleY;
      points.push([it.x+u*g.c-v*g.s,it.y+u*g.s+v*g.c]);
    }
    for(let j=uid+1;j<this.geom.length;j++){
      const p=this.geom[j];if(Math.abs(p.item.x-it.x)>=p.hx+g.hx||Math.abs(p.item.y-it.y)>=p.hy+g.hy)continue;
      const bits=new Uint32Array(Math.ceil(points.length/32));let n=0;
      points.forEach(([x,y],i)=>{if(hit(p,x,y)){bits[i>>>5]|=1<<(i&31);n++}});if(n)covers.push({j,bits});
    }
    const result={all:points.length,covers};this.cache.set(uid,result);return result;
  }
  covered(uid){
    const {all,covers}=this.coverData(uid);if(!covers.length)return false;
    const union=new Uint32Array(Math.ceil(all/32));let n=0;
    for(const {j,bits} of covers)if(this.room.has(j))for(let i=0;i<bits.length;i++)union[i]|=bits[i];
    for(let b of union)while(b){n++;b&=b-1}
    return n/Math.max(1,all)>=.045;
  }
  direct(){return [...this.room].some(i=>this.box(this.items[i].group)>=0&&!this.covered(i));}
  settle(){
    let changed=true;
    while(changed){changed=false;
      for(const b of this.boxes)if(this.order(b)&&b.count>=this.order(b).count){this.assign(b);changed=true;}
      for(const uid of [...this.tray]){
        const b=this.boxes[this.box(this.items[uid].group)];if(b&&b.count<this.order(b).count){
          b.count++;this.tray.splice(this.tray.indexOf(uid),1);this.delivered++;changed=true;
        }
      }
    }
  }
  tapAt(x,y){
    if(this.state!=='playing')return {kind:'ended'};
    for(let j=this.geom.length-1;j>=0;j--)if(this.room.has(j)&&hit(this.geom[j],x,y))return this.tap(j);
    return {kind:'blank'};
  }
  tap(j){
    if(this.state!=='playing'||!this.room.has(j))return {kind:'ended'};
    if(this.covered(j))return {kind:'blocked',j};
    const b=this.boxes[this.box(this.items[j].group)];
    if(!b&&this.tray.length===5)return {kind:'full',j};
    this.room.delete(j);this.moves++;
    if(b){b.count++;this.delivered++;}else this.tray.push(j);
    this.peak=Math.max(this.peak,this.tray.length);this.settle();
    if(this.delivered===this.items.length)this.state='win';
    else if(this.tray.length===5&&(this.level.rule==='strict'||!this.direct()))this.state='lose';
    const result={kind:b?'box':'tray',j};this.log.push(result);return result;
  }
}
