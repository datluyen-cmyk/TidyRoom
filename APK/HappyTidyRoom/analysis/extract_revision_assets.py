import sys,pathlib,json,collections
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom\analysis');sys.path.insert(0,str(r/'vendor'));import UnityPy
from PIL import Image,ImageDraw
c=json.loads((r/'mono/resources.assets_7861.json').read_text(encoding='utf8'));groups={x['value']:x for x in c['groups']};subs={x['value']:x for x in c['subGroups']};items=collections.defaultdict(list)
for x in c['items']:items[x['subGroup']].append(x)
used=set()
for p in (r/'unity').glob('*level_*.txt'):
 try:d=json.loads(p.read_text(encoding='utf8'))
 except:continue
 used.update(x['id'] for x in d['content'])
reps={k:next((x['id'] for x in v if x['id'] in used),v[0]['id']) for k,v in items.items()}
iconnames=['NewBooster_Icon_Vaccum','NewBooster_Icon_Clear','GP_Box_Unlock','AddSlot_Img','GP_Slot_Unlock','Icon_HiddenPassenger','Unlock_Booster_Text_HiddenPassenger','GP_Slot_Warning','GP_Icon_RainbowBox','GP_Icon_RainbowBox_Front']
e=UnityPy.load(str(r/'data.unity3d'));found={};out=r/'visuals';repids=set(reps.values())
for o in e.objects:
 if o.type.name=='Sprite':
  d=o.read();n=d.m_Name
  if n in repids or n in iconnames:
   im=d.image.convert('RGBA');found[n]=im
   if n in iconnames:im.save(out/(n+'.png'))
 # Find actual sprites on the Extra Box / Extra Slot UI prefabs.
 if o.type.name=='MonoBehaviour' and o.assets_file.name=='resources.assets':
  try:
   d=o.read_typetree(check_read=False)
   if d.get('m_GameObject',{}).get('m_PathID') in [6582,6410] and 'm_Sprite' in d:print('EXTRA ICON',d['m_GameObject'],d['m_Sprite'])
  except:pass
for k,n in reps.items():
 im=found[n].copy();im.thumbnail((110,100));canvas=Image.new('RGBA',(120,110),(255,255,255,0));canvas.alpha_composite(im,((120-im.width)//2,(110-im.height)//2));canvas.save(out/f'category_{k}.png')
rows=[]
for k,v in sorted(items.items(),key=lambda kv:(subs[kv[0]]['group'],kv[0])):
 rows.append({'id':k,'groupId':subs[k]['group'],'group':groups[subs[k]['group']]['folder'],'category':subs[k]['folder'],'name':subs[k]['name'],'count':len(v),'used':sum(x['id'] in used for x in v),'example':reps[k]})
(r/'category-object.json').write_text(json.dumps({'categories':rows,'total':sum(x['count'] for x in rows),'used':len(used),'groups':len(set(x['groupId'] for x in rows))},ensure_ascii=False,indent=2),encoding='utf8')
canvas=Image.new('RGB',(1000,450),'#F6F6F6');draw=ImageDraw.Draw(canvas)
for i,n in enumerate(iconnames):
 if n not in found:continue
 im=found[n].copy();im.thumbnail((180,160));x=i%5*200;y=i//5*225;canvas.paste(im,(x+(200-im.width)//2,y+10),im);draw.text((x+5,y+180),n[:28],fill='black')
canvas.save(out/'revision-icons.png');print('Saved',len(rows),'category thumbnails and',len(iconnames),'icons')
