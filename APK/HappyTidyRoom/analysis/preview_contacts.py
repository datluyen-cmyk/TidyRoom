from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
p=Path('analysis/previews');files=sorted(p.glob('*.png'))
for start in range(0,len(files),4):
 tiles=[]
 for f in files[start:start+4]:
  im=Image.open(f).convert('RGB');im=im.crop((0,0,im.width,min(im.height,700)));im.thumbnail((880,560));tile=Image.new('RGB',(900,600),'#FFFFFF');tile.paste(im,(10,35));ImageDraw.Draw(tile).text((12,10),f.stem,fill='#000000');tiles.append(tile)
 canvas=Image.new('RGB',(1800,1200),'#E1E5E8')
 for i,im in enumerate(tiles):canvas.paste(im,((i%2)*900,(i//2)*600))
 canvas.save(p/f'contact-{start//4+1}.png')
print([(f.name,Image.open(f).size) for f in files])
