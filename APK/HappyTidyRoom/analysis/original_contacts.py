from PIL import Image,ImageDraw
from pathlib import Path
p=Path('analysis/original-format-previews')
for st in range(0,14,4):
 files=sorted(p.glob('*.png'))[st:st+4];canvas=Image.new('RGB',(1800,1200),'#E5E5E5')
 for i,f in enumerate(files):
  im=Image.open(f).convert('RGB');im=im.crop((0,0,im.width,min(im.height,950)));im.thumbnail((880,560));canvas.paste(im,((i%2)*900+10,(i//2)*600+25));ImageDraw.Draw(canvas).text(((i%2)*900+10,(i//2)*600+5),f.stem,fill='#000000')
 canvas.save(p/f'contact-{st//4+1}.png')
