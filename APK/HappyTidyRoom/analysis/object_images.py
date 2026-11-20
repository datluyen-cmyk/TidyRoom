import sys,json
from pathlib import Path
r=Path(r'D:\APK Works\HappyTidyRoom\analysis');sys.path.insert(0,str(r/'vendor'))
import UnityPy
from PIL import Image,ImageDraw
e=UnityPy.load(str(r/'data.unity3d'))
names={'GP_Slot','GP_Frame_Slot','GP_Box0','GP_Box1','GP_Box_0_Front','GP_Box_Unlock'}
found={}
level={o.path_id:o for o in e.objects if o.assets_file.name=='level1'}
def walk(pid):
 d=level[pid].read_typetree(check_read=False)
 go=d.get('m_GameObject',{}).get('m_PathID')
 if go:
  gd=level[go].read_typetree(check_read=False)
  print('GO',pid,gd.get('m_Name'),[(level[x['component']['m_PathID']].type.name,x['component']['m_PathID']) for x in gd.get('m_Component',[])])
 for o in level.values():
  if o.type.name!='MonoBehaviour':continue
  a=o.read_typetree(check_read=False)
  if a.get('m_GameObject',{}).get('m_PathID')==go and 'm_Sprite' in a: print('IMAGE',pid,a['m_Sprite'])
 for child in d.get('m_Children',[]): walk(child['m_PathID'])
for pid in [349,379,557]:walk(pid)
for o in e.objects:
 if o.assets_file.name=='level1' and o.type.name=='MonoBehaviour':
  d=o.read_typetree(check_read=False)
  if d.get('m_GameObject',{}).get('m_PathID') in [9,43,41,62,146,133] and 'm_Sprite' in d:
   print(o.path_id,json.dumps({k:v for k,v in d.items() if k in ['m_Sprite','m_GameObject']},ensure_ascii=False))
 if o.type.name=='Sprite':
  d=o.read()
  if d.m_Name in names:
   im=d.image.convert('RGBA');im.save(r/'visuals'/f'{d.m_Name}.png');found[d.m_Name]=im
canvas=Image.new('RGB',(900,240),'#F5F5F5');draw=ImageDraw.Draw(canvas)
for i,(n,im) in enumerate(found.items()):
 im.thumbnail((140,180));canvas.paste(im,(i*150,10),im);draw.text((i*150,205),n,fill='black')
canvas.save(r/'visuals/object-contact.png')
slot=found['GP_Slot'].copy();slot.thumbnail((32,32))
tray=Image.new('RGBA',(180,42),(255,255,255,0))
for i in range(5):tray.alpha_composite(slot,(i*36+2,5))
tray.save(r/'visuals/WaitingSlots_Reference.png')
