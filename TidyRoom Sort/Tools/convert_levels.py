"""RoomSort -> Happy schema + lossless test metadata. Python 3 + Pillow.
Run prepare_sources.mjs once before this script. Mapping is deliberately editable.
"""
from pathlib import Path
import argparse, collections, json, math, re, shutil, sys, zipfile
from PIL import Image
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,separators=(',',':')),encoding='utf8')
def norm(s): return re.sub('[^a-z0-9]','',s.lower()).rstrip('s')
# Explicit semantic equivalences for early boards and common categories.
ALIASES={1:41041,2:56010,3:56007,4:41060,5:43009,6:41042,7:41022,8:43007,9:36002,10:56001,11:41027,12:37003,13:51005,14:41061,15:41032,16:41058,17:41004,18:41044,19:47008,20:49001,21:61005,22:41045,23:41036,24:41065,25:41015,26:38004,27:41016,28:41025,29:46001,30:41026,31:41059,32:56006,33:41006,34:57009,35:41012,36:34007,37:47003,38:47003,39:41020,40:47012,41:47003,42:41001,43:41024,44:67003,45:47013,46:47007,47:41011,48:45007,49:44003,50:41002,51:41007,52:41004,53:51009,54:40003,55:51002,56:51001,57:61006,59:76004,60:51008,61:51006,62:41070,63:46003,64:41057,65:46004,66:46002,67:41056,68:75003,69:37001,70:41062,71:41039,72:41023,73:41018,74:37003,75:41074,76:43009,78:41013,79:47006,80:47008,81:39001,82:41035,83:41016,84:41013,85:41043,86:41020,87:59003,88:43008,89:41035,91:41058,93:35001,94:38002,95:41047,96:43005,97:35001,100:41060,101:41004,102:41023,103:41065,104:40003,105:41036,106:41059,107:41041,108:41027,109:41026,110:56007,111:41061,200:41046,202:41072,205:41049,207:41060,208:41050,210:56003,211:56003,215:43011,216:43010,217:65001,218:41053,219:65003,220:36010,221:54004,222:42007,223:41010,224:52002,225:52006,226:52003,227:52008,228:75003,230:41037,231:38003,232:38003,234:41063,235:57009,236:56002,237:59002,250:53001,251:53002,256:41066,272:47009,274:41068,275:35002,276:35002,277:41047,278:35003,279:41060,300:41021,301:41011,302:61005,303:42004,305:64004,306:58007,307:41069,309:38005,310:41025,311:41027,312:38004,313:38002,315:42008,316:42007,317:42011,318:42012,319:42001,321:47008,322:47011,325:47005,326:42003,328:51007,329:51007,330:41040,331:41045,332:67003,337:41073,340:41001,342:75003,343:71006,344:41031,345:48001,346:48002,347:41055,349:41029,357:45008,358:45002,359:45001,360:45006,362:45010,363:63006,364:45009,365:75001,366:34007,369:71001,372:44001,373:64004,374:65003,377:41009,381:41054,382:41058,383:41058,384:41054,385:41058,386:41058,387:35001,388:56007,389:56004,390:35002,392:44003,393:56009,394:52004,395:52003,396:52008,500:56003,501:56008,502:56004,503:56001,506:47002,507:47010,508:42003,509:41060,510:43005,511:40003,513:40001,514:40003,516:41017,518:41030,600:50001,601:50002,602:55002,603:55003,604:50002,605:50002,606:34006,607:34003,608:34007,609:34004,610:34002,611:41013,612:76001,614:56003,615:56003,616:56003,617:56003,618:56003,619:61003,620:41068,623:47003,626:47009,627:67005,628:67006,629:43003,636:34007,641:42004,642:62004,643:43003,644:41009,645:35002,646:72007,647:72003,648:72002,649:66003,651:41007,652:72006,653:64002,655:47008,656:41046,700:56010,701:41019,702:41044,704:41008,706:38005,707:71004,708:42006,709:42009,710:42008,711:42010,712:42003}
# Broad source categories require a design choice; mark them explicitly.
PROXY={9,15,19,35,36,38,39,48,53,79,80,86,89,94,95,102,103,210,211,219,256,316,340,342,343,373,395,500,511,513,514,602,604,605,614,615,616,617,618,636,641,653,655,700,702,706,712}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--happy-root',default='D:/APK Works/HappyTidyRoom');ap.add_argument('--room-root',default='D:/APK Works/RoomSort');ap.add_argument('--strict',action='store_true',help='Return failure if any board requires mapping review');a=ap.parse_args()
    hr=Path(a.happy_root);rr=Path(a.room_root);src=read(ROOT/'Tools/Source/room.json');cat=read(hr/'analysis/mono/resources.assets_7861.json');happy=read(rr/'analysis/happy-levels.json')
    config=read(hr/'analysis/mono/resources.assets_10789.json')
    mapScales={m['key']:{x['type']:x['scale'] for x in m['itemScales']} for m in config['maps']}
    out=ROOT/'Assets/StreamingAssets/TidyRoom';out.mkdir(parents=True,exist_ok=True)
    assetdir=out/'Art/Happy';assetdir.mkdir(parents=True,exist_ok=True)
    zpath=hr/'outputs/happy-tidy-room-assets/Happy Tidy Room - Object Assets.zip'
    with zipfile.ZipFile(zpath) as z:
        for f in z.infolist():
            if f.filename.lower().endswith('.png'):
                dst=assetdir/Path(f.filename).name
                if not dst.exists():dst.write_bytes(z.read(f))
    items={x['id']:x for x in cat['items']};bygroup=collections.defaultdict(list)
    for x in cat['items']:bygroup[x['subGroup']].append(x['id'])
    groups={x['value']:x['folder'] for x in cat['subGroups'] if x['value'] in bygroup}
    mappingfile=ROOT/'Tools/category-map.json'
    if mappingfile.exists(): mapping=read(mappingfile)
    else:
        mapping={}
        for t in sorted({int(i['id'].split('-')[0]) for l in src['levels'] for i in l['content']}):
            name=src['translations'].get(f'type.{t}',str(t));target=ALIASES.get(t)
            if target is None:
                matches=[g for g,n in groups.items() if norm(n)==norm(name)]
                if len(matches)==1:target=matches[0]
            mapping[str(t)]={'sourceName':name,'happyType':target,'happyName':groups.get(target,''),'status':'proxy' if t in PROXY else 'mapped' if target else 'unmapped'}
        # The tissue tutorial's custom category labels are registered outside base i18n.
        for t,target in {16000:41015,16001:41006,16002:41025,16003:41065,16004:41015}.items():
            if str(t) in mapping:mapping[str(t)].update(happyType=target,happyName=groups[target],status='proxy')
        write(mappingfile,mapping)
    manifest=[];report=[];metadata={};native=ROOT/'Converted/HappyLevels';native.mkdir(parents=True,exist_ok=True)
    assetCache={}
    def shape(path):
        if path not in assetCache:
            with Image.open(path) as im:
                im=im.convert('RGBA');w,h=im.size;alpha=im.getchannel('A');alpha.thumbnail((40,40));mw,mh=alpha.size
                assetCache[path]={'width':w,'height':h,'maskW':mw,'maskH':mh,'alpha':[1 if v>32 else 0 for v in alpha.getdata()]}
        return assetCache[path]
    def export(key,label,source,l):
        p=out/'Levels'/f'{key}.json';write(p,l);manifest.append({'key':key,'label':label,'source':source,'file':f'Levels/{key}.json','review':bool(l.get('issues'))})
    for l in src['levels']:
        key=l['key'];types=sorted({o['type'] for o in l['order']});issues=[];mapped={};seen={}
        for t in types:
            m=mapping[str(t)];g=m['happyType'];mapped[t]=g
            if not g:issues.append(f'Unmapped category {t}: {m["sourceName"]}')
            elif m['status']=='proxy':issues.append(f'Proxy category {t}: {m["sourceName"]} -> {groups[g]}')
            if g in seen and g:issues.append(f'Merged Happy category {g}: source {seen[g]} and {t} must stay separate')
            seen[g]=t
        orders=[{'type':mapped[o['type']] or 900000+o['type'],'sourceType':o['type'],'label':mapping[str(o['type'])]['sourceName'],'count':o['count'],'box':1000+j,'diff':0} for j,o in enumerate(l['order'])]
        available=collections.defaultdict(list)
        for o in orders:available[o['sourceType']].extend([o['box']]*o['count'])
        cursors=collections.Counter();content=[];assign={}
        for uid,i in enumerate(l['content']):
            t=int(i['id'].split('-')[0]);g=mapped[t];s=src['shapes'][i['id']]
            if g:
                # Stable ID mapping independent of UID, level and Python hash randomization.
                choices=sorted(bygroup[g]);n=int(i['id'].split('-')[1]);aid=mapping[str(t)].get('items',{}).get(i['id'],choices[(n-1)%len(choices)])
                if aid not in choices:raise ValueError(f'Invalid item override {i["id"]} -> {aid} for category {g}')
                art=f'Art/Happy/{aid}.png'
            else:
                aid=i['id'];art=f'Art/Room/{aid}.png';dst=out/art;dst.parent.mkdir(parents=True,exist_ok=True)
                source=rr/'analysis/www/assets'/src['itemFiles'][aid]
                # Source files may contain WebP despite a .png suffix. Unity LoadImage needs PNG/JPEG.
                if not dst.exists():Image.open(source).convert('RGBA').save(dst,format='PNG')
            sh=shape(out/art);factor=min(s['w']/sh['width'],s['h']/sh['height'])
            j=cursors[t];cursors[t]+=1
            content.append({**i,'id':aid,'sourceId':i['id'],'sourceType':t,'type':g or 900000+t,'box':available[t][j],'uid':uid,'art':art,'width':sh['width']*factor,'height':sh['height']*factor,'sourceWidth':s['w'],'sourceHeight':s['h'],'poly':s['poly'],**{k:sh[k] for k in ['maskW','maskH','alpha']}})
        assert all(cursors[t]==len(available[t]) for t in available),'Item/order mismatch'
        # Preserve source room: props sit against this geometry, Happy backdrop changes furniture placement.
        bgFile=l.get('bgFile',str(l.get('bg'))+'.jpg');bgrel=src['backgrounds'].get(bgFile)
        bg=f'Art/RoomBG/{Path(bgFile).stem}.jpg'
        if not bgrel:raise ValueError(f'Missing background {bgFile}')
        dest=out/bg;dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():Image.open(rr/'analysis/www/assets'/bgrel).convert('RGB').save(dest,format='JPEG',quality=95,subsampling=0)
        converted={'key':key,'levelName':str(l['level']),'name':f'RoomSort {l["level"]}','bg':bg,'bgPosX':l.get('bgPosX',0),'order':orders,'content':content,'issues':issues,'proof':l.get('proof',[]),'source':'RoomSort','coverageMode':'source','blockThreshold':.045}
        export(key,f'Room {l["level"]}'+(' / '+key if key.startswith('ladder') else ' / tutorial' if 'tissue' in key else ''),'RoomSort',converted)
        # Native Happy output keeps its own schema; companion report tells whether safe to load unchanged.
        pure={'bgPosX':l.get('bgPosX',0),'bg':f'HT_BG_{min(l["level"],60):02}','levelName':str(l['level']),'order':[{k:o[k] for k in ['type','count','box','diff']} for o in orders],'content':[{**{k:i[k] for k in ['id','x','y','angle','box']},'scaleX':i['scaleX']*i['width']/shape(out/i['art'])['width'],'scaleY':i['scaleY']*i['height']/shape(out/i['art'])['height']} for i in content]}
        target=native/('CatalogCompatible' if not issues else 'NeedsReview')/f'{key}.json';write(target,pure)
        stale=native/('NeedsReview' if not issues else 'CatalogCompatible')/f'{key}.json'
        if stale.exists():stale.unlink()
        report.append({'key':key,'items':len(content),'boxes':len(orders),'catalogCompatible':not issues,'layoutNeedsRetest':True,'issues':issues})
    for n,l in enumerate(happy):
        key=f'happy_{n+1:03}';content=[]
        for uid,i in enumerate(l['content']):
            sh=shape(assetdir/(i['id']+'.png'));t=items[i['id']]['subGroup']
            scale=mapScales.get(l['bg'],{}).get(t,1)
            content.append({**i,'uid':uid,'type':t,'sourceType':t,'art':f'Art/Happy/{i["id"]}.png',**sh,'width':sh['width']*scale,'height':sh['height']*scale})
        orders=[{**o,'sourceType':o['type'],'label':groups[o['type']]} for o in l['order']]
        export(key,f'Happy {l["levelName"]} / {l["_file"]}','Happy',{**l,'key':key,'source':'Happy','bg':f'Art/HappyBG/{l["bg"]}.jpg','order':orders,'content':content,'coverageMode':'art','blockThreshold':.045,'issues':[]})
    write(out/'index.json',{'levels':manifest});write(ROOT/'Converted/conversion-report.json',report)
    write(ROOT/'Converted/mapping-summary.json',{'categories':len(mapping),'mapped':sum(m['status']=='mapped' for m in mapping.values()),'proxy':sum(m['status']=='proxy' for m in mapping.values()),'unmapped':{t:m for t,m in mapping.items() if not m['happyType']},'catalogCompatible':sum(x['catalogCompatible'] for x in report),'boards':len(report)})
    print(f'Exported {len(manifest)} boards; {sum(x["catalogCompatible"] for x in report)}/{len(report)} Room boards catalog-compatible without category review. All changed layouts require retest. Happy art: {len(items)} assets.')
    if a.strict and any(x['issues'] for x in report):return 2
    return 0
if __name__=='__main__':sys.exit(main())
