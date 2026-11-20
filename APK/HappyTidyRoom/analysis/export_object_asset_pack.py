import sys,json,re,io,zipfile,collections,time
from pathlib import Path
root=Path(r'D:\APK Works\HappyTidyRoom');a=root/'analysis'
sys.path.insert(0,str(a/'vendor'))
import UnityPy
from PIL import Image

catalog=json.loads((a/'mono/resources.assets_7861.json').read_text(encoding='utf8'))
groups={x['value']:x for x in catalog['groups']}
categories={x['value']:x for x in catalog['subGroups']}
items={x['id']:x for x in catalog['items']}
assert len(items)==len(catalog['items'])==2863
def safe(s):
 return re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',s).rstrip('. ')
paths={}
for itemid,x in items.items():
 context=safe(groups[x['group']]['folder'])
 category=safe(categories[x['subGroup']]['folder'])
 paths[itemid]=f'Happy Tidy Room - Object Assets/{context}/{category}/{safe(itemid)}.png'
assert len(set(paths.values()))==len(items)
out=root/'outputs/happy-tidy-room-assets';out.mkdir(parents=True,exist_ok=True)
target=out/'Happy Tidy Room - Object Assets.zip'
tmp=out/'Happy Tidy Room - Object Assets.partial.zip'
env=UnityPy.load(str(a/'data.unity3d'))
seen=set();dimensions={};started=time.monotonic()
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=1) as z:
 for obj in env.objects:
  if obj.type.name!='Sprite':continue
  sprite=obj.read();name=sprite.m_Name
  if name not in items or name in seen:continue
  image=sprite.image.convert('RGBA')
  assert image.width>0 and image.height>0
  data=io.BytesIO();image.save(data,format='PNG')
  z.writestr(paths[name],data.getvalue())
  seen.add(name);dimensions[name]=[image.width,image.height]
  if len(seen)%250==0:print(f'Exported {len(seen)}/{len(items)} images',flush=True)
assert seen==items.keys(),f'Missing {items.keys()-seen}'
with zipfile.ZipFile(tmp) as z:
 assert len(z.infolist())==2863
 assert z.testzip() is None
 assert set(z.namelist())==set(paths.values())
 for entry in z.infolist():
  with z.open(entry) as f:
   im=Image.open(f);assert im.format=='PNG';im.verify()
tmp.replace(target)
report={'images':len(seen),'contexts':len(set(x['group'] for x in items.values())),
 'categories':len(set(x['subGroup'] for x in items.values())),
 'sizeMB':round(target.stat().st_size/1024/1024,2),'output':str(target),
 'elapsedSeconds':round(time.monotonic()-started,1),'dimensions':dimensions}
(a/'object-asset-pack-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k!='dimensions'},ensure_ascii=False),flush=True)
