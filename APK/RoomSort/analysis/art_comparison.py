from pathlib import Path
import json,zipfile,io
from PIL import Image,ImageDraw,ImageFont
r=Path(r'D:\APK Works\RoomSort');a=r/'analysis';w=a/'www/assets'
p=json.loads((a/'room-content-expanded.json').read_text(encoding='utf8'))
theme=json.loads((w/'art/theme_trials_20261112/manifest.json').read_text())['themes']['bright_update1111_v1']['items']
h=json.loads(Path(r'D:\APK Works\HappyTidyRoom\analysis\category-object.json').read_text(encoding='utf8'))
hc=json.loads(Path(r'D:\APK Works\HappyTidyRoom\analysis\mono/resources.assets_7861.json').read_text(encoding='utf8'))
z=zipfile.ZipFile(r'D:\APK Works\HappyTidyRoom\outputs\happy-tidy-room-assets\Happy Tidy Room - Object Assets.zip')
zipnames={Path(n).stem:n for n in z.namelist()}
out=r/'outputs/roomsort-comparison';out.mkdir(parents=True,exist_ok=True)
canvas=Image.new('RGB',(1290,760),'#FFFFFF');d=ImageDraw.Draw(canvas)
f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
for col,title in enumerate(['RoomSort - standard','RoomSort - bright skin','Happy Tidy Room']):d.text((col*430+20,18),title,font=f,fill='#24352D')
rows=[('Handbags','28',41025),('Shoes','16',41058),('Pants','1',41041),('Socks','14',41061)]
def paste(im,x,y):
 im=im.convert('RGBA');im.thumbnail((90,110));canvas.paste(im,(int(x+(100-im.width)/2),int(y+(115-im.height)/2)),im)
for row,(label,typ,hid) in enumerate(rows):
 y=65+row*170
 d.rectangle((0,y,1289,y+165),fill=['#F3F7FA','#F8F7F0'][row%2])
 ids=sorted([id for id in p['base']['items'] if id.startswith(typ+'-') and id in theme],key=lambda s:int(s.split('-')[1]))[:4]
 hids=[x['id'] for x in hc['items'] if x['subGroup']==hid][:4]
 for col in range(3):d.text((col*430+16,y+8),label,font=small,fill='#435348')
 for i,id in enumerate(ids):
  paste(Image.open(w/p['expanded']['itemFiles'][id]),15+i*102,y+35)
  paste(Image.open(w/theme[id]),445+i*102,y+35)
 for i,id in enumerate(hids):paste(Image.open(io.BytesIO(z.read(zipnames[id]))),875+i*102,y+35)
canvas.save(out/'art-comparison.png')
print(out/'art-comparison.png')
