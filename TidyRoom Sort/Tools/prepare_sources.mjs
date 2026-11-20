import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const root=process.argv[2]||'D:/APK Works/RoomSort/analysis';
const payload=JSON.parse(fs.readFileSync(root+'/room-content-expanded.json','utf8'));
const {applyDeal}=await import(pathToFileURL(root+'/www/game/src/services/deal-variant.js'));
const levels=payload.base.levels.map(l=>({...l,key:`room_${l.level.toString().padStart(3,'0')}`}));
for(const [variant,v] of Object.entries(payload.variants))for(const [n,p] of Object.entries(v.proofs??{})) {
 const l=applyDeal(payload.base.levels.find(l=>l.level===+n),variant);
 levels.push({...l,key:`${variant}_${n}`,proof:p.path});
}
const my=payload.rooms.my_room;
levels.push({...my.level,key:'room_tissue_001'});
const en=JSON.parse(fs.readFileSync(root+'/www/assets/i18n/en.json','utf8'));
const translations={...en,...my.translations?.en};
fs.mkdirSync(new URL('./Source/',import.meta.url),{recursive:true});
fs.writeFileSync(new URL('./Source/room.json',import.meta.url),JSON.stringify({levels,shapes:payload.expanded.catalog.items,itemFiles:payload.expanded.itemFiles,backgrounds:payload.expanded.backgrounds,translations}));
console.log(`Prepared ${levels.length} RoomSort boards`);
