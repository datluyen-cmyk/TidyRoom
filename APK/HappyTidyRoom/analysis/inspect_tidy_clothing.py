from pathlib import Path
import sys,json,re,collections
root=Path(r'D:/APK Works/HappyTidyRoom')
sys.path.insert(0,str(root/'analysis/vendor'))
import UnityPy
from PIL import Image,ImageDraw,ImageFont,ImageOps
p=Path(r'D:/APK Works/Tidy Room/analysis')
out=root/'analysis/tidy-clothing-review'
out.mkdir(exist_ok=True)
shape=json.loads((p/'RoomItemShapes.txt').read_text(encoding='utf8'))
index=json.loads((p/'unity-index.json').read_text(encoding='utf8'))
natur=lambda name:tuple(map(int,name.split('-')))
groups=[['1','24','31','23'],['103','105','106','107','12','74','42'],['248','249','516','518','347','353']]
alltype={i for g in groups for i in g}
bg_names={'bedroom','kids_bedroom','wedding_bedroom','aquarium_bedroom','living_room','clothing_store'}
selected=[x for x in index if x['type']=='Sprite' and (x['name'] in bg_names or re.fullmatch(r'\d+-\d+',x['name']) and x['name'].split('-')[0] in alltype)]
obj={o.path_id:o for o in UnityPy.load(str(p/'art-Tidy-Room_57_apkcube/datapack.unity3d')).objects if o.type.name=='Sprite' and o.assets_file.name=='resources.assets'}
images={}
for x in selected:
 d=obj[x['id']].read(); assert d.m_Name==x['name']; a=d.image.convert('RGBA'); images[x['name']]=a; a.save(out/(x['name']+'.png'))
font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',17)
for n,g in enumerate(groups,1):
 names=sorted([x for x in images if '-' in x and x.split('-')[0] in g],key=natur)
 canvas=Image.new('RGB',(920,120*((len(names)+7)//8)), '#eeeae5');draw=ImageDraw.Draw(canvas)
 for i,name in enumerate(names):
  x=i%8*115;y=i//8*120; draw.rectangle((x+2,y+2,x+112,y+115),fill='#f8f6f2'); a=images[name].copy();a.thumbnail((104,91)); canvas.paste(a,(x+(115-a.width)//2,y+4+(91-a.height)//2),a);draw.text((x+7,y+95),name,fill='#292828',font=font)
 canvas.save(out/f'clothes-{n}.png')
names=sorted(bg_names & images.keys());canvas=Image.new('RGB',(1080,425*((len(names)+2)//3)),'#edeae5');draw=ImageDraw.Draw(canvas)
for i,name in enumerate(names):
 x=i%3*360;y=i//3*425;a=images[name].copy();a.thumbnail((350,390));canvas.paste(a,(x+(360-a.width)//2,y+4),a);draw.text((x+7,y+397),name,fill='#292828',font=font)
canvas.save(out/'rooms.png')
print('Exported',len(images)-len(names),'clothing/towel group sprites;',len(names),'backgrounds. Shapes matched:',sum(x in shape for x in images));print(out)
