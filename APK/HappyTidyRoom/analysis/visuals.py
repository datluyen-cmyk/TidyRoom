import sys,pathlib,json
r=pathlib.Path('analysis');sys.path.insert(0,str(r/'vendor'));import UnityPy
from PIL import Image,ImageDraw,ImageFont
names=['HT_BG_01','HT_BG_04','Hanger_3','Shoes_6','Trouser_17','Socks_4','Scrap_Paper_5','GP_Icon_Booster_Magnet','GP_Icon_Booster_Clear','GP_Icon_RainbowBox_Front']
e=UnityPy.load(str(r/'data.unity3d'));out=r/'visuals';out.mkdir(exist_ok=True);found={}
for o in e.objects:
 if o.type.name=='Sprite':
  d=o.read()
  if d.m_Name in names:
   try:im=d.image;im.save(out/(d.m_Name+'.png'));found[d.m_Name]=im
   except Exception as ex:print(str(ex)[:100])
canvas=Image.new('RGB',(1000,540),'#F5F1EB');draw=ImageDraw.Draw(canvas)
for i,(name,im) in enumerate(found.items()):
 x=(i%5)*200;y=(i//5)*270;im=im.copy();im.thumbnail((180,220));canvas.paste(im,(x+(200-im.width)//2,y+10),im if im.mode=='RGBA' else None);draw.text((x+10,y+240),name,fill='#222222')
canvas.save(out/'asset-contact-sheet.png');print('IMAGES',list(found))
# compact evidence list for all relevant objects except the giant catalog
idx=json.loads((r/'mono-index.json').read_text(encoding='utf8'));outidx=[x for x in idx if not x['class'].startswith(('HappyTidy.CatalogSpriteRef','TMPro','UnityEngine','Unity.Services','Spine','Coffee','DG'))];(r/'game-object-index.json').write_text(json.dumps(outidx,ensure_ascii=False,indent=2),encoding='utf8')
