from pathlib import Path
import sys,json
R=Path(r'D:/APK Works/HappyTidyRoom'); T=Path(r'D:/APK Works/Tidy Room/analysis'); S=Path(r'D:/APK Works/RoomSort/analysis')
sys.path.insert(0,str(R/'analysis/vendor'))
import UnityPy
from PIL import Image,ImageOps,ImageDraw
import numpy as np
idx=json.loads((T/'unity-index.json').read_text(encoding='utf8')); bg_names=set(json.loads((T/'RoomBackgroundLegacyNames.txt').read_text(encoding='utf8')).values()); data=json.loads((S/'room-content-expanded.json').read_text(encoding='utf8')); room=data['base']['levels']; paths=data['expanded']['backgrounds']; dest=R/'analysis/level-studio-research';dest.mkdir(exist_ok=True)
def vec(im):
 a=np.asarray(im.convert('RGB').resize((45,45)),dtype='float32');return a
tid={}; meta={}; root=UnityPy.load(str(T/'art-Tidy-Room_57_apkcube/datapack.unity3d')); wanted={x['id']:x['name'] for x in idx if x['type']=='Sprite' and x['name'] in bg_names and x['file']=='resources.assets'}
for o in root.objects:
 if o.type.name=='Sprite' and o.assets_file.name=='resources.assets' and o.path_id in wanted:
  d=o.read(); im=d.image; tid[d.m_Name]=vec(im);meta[d.m_Name]=(im.size,o.path_id);im.thumbnail((220,225));im.save(dest/(d.m_Name+'.png'))
res=[]
for l in room:
 q=S/'www/assets'/paths.get(l['bgFile'],'missing');
 if not q.is_file(): continue
 im=Image.open(q); v=vec(im); ranks=sorted((float(np.mean(np.abs(v-b))),n) for n,b in tid.items());err,n=ranks[0]
 res.append(dict(level=l['level'],path=str(q),roomSize=im.size,tidy=n,tidySize=meta[n][0],sprite=meta[n][1],mae=round(err,2),sizeRatio=round((im.width/im.height)/(meta[n][0][0]/meta[n][0][1]),4),runnerUp=ranks[1][0]))
(dest/'matches.json').write_text(json.dumps(res,indent=2),encoding='utf8'); print('pair candidates:',len(res), 'same aspect + MAE < 12:',sum(x['mae']<12 and abs(x['sizeRatio']-1)<.015 for x in res)); print([(x['level'],x['tidy'],x['mae'],x['sizeRatio']) for x in res[:25]])
res=sorted(res,key=lambda x:x['level'])[:12]; a=Image.new('RGB',(1120,185*((len(res)+2)//3)),'#eeeae5'); d=ImageDraw.Draw(a)
for i,x in enumerate(res):
 xx=i%3*370;yy=i//3*185
 for j,im in enumerate([Image.open(x['path']),Image.open(dest/(x['tidy']+'.png'))]):
  im=im.convert('RGB');im.thumbnail((177,153));a.paste(im,(xx+j*182+(177-im.width)//2,yy))
 d.text((xx+4,yy+155),f"{x['level']} | {x['tidy']} | error {x['mae']}",fill='black')
a.save(dest/'pairs.png')
