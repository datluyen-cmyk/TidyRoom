import sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
r=Path(r'D:\APK Works\HappyTidyRoom\analysis');sys.path.insert(0,str(r/'vendor'))
import UnityPy
names={'Tutorial_Hand_1','Tutorial_Hand_2','Tutorial_Hand_3','GP_Icon_Tutorial_2','GP_Icon_Tutorial_3'}
for o in UnityPy.load(str(r/'data.unity3d')).objects:
 if o.type.name=='Sprite':
  s=o.read()
  if s.m_Name in names:s.image.save(r/'visuals'/f'{s.m_Name}.png')
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',15)
def picture(name,x,y,w,h):
 im=Image.open(r/'visuals'/f'{name}.png').convert('RGBA');im.thumbnail((w,h));canvas.alpha_composite(im,(int(x+(w-im.width)/2),int(y+(h-im.height)/2)))
def arrow(x,y):
 draw.line((x,y,x+62,y),fill='#687D70',width=4);draw.polygon([(x+62,y),(x+50,y-8),(x+50,y+8)],fill='#687D70')
for mode in ['core','vacuum','broom','extra']:
 canvas=Image.new('RGBA',(800,210),'#F7FAF8');draw=ImageDraw.Draw(canvas)
 draw.text((14,10),'ILLUSTRATION',font=small,fill='#687D70')
 if mode=='core':
  picture('Hanger_3',35,47,105,110);picture('Tutorial_Hand_1',100,110,65,82);arrow(185,103)
  picture('GP_Box0',285,48,135,110);draw.text((308,165),'Hanger',font=font,fill='#273D30')
  draw.text((460,63),'Tap to collect matching items',font=font,fill='#273D30')
  draw.text((460,107),'Check the category label!',font=font,fill='#273D30')
 elif mode=='vacuum':
  picture('NewBooster_Icon_Vaccum',55,45,130,120);picture('Tutorial_Hand_1',145,110,65,82);arrow(240,103)
  picture('GP_Box0',340,48,135,110)
  draw.text((510,86),'Fill a box instantly!',font=font,fill='#273D30')
 elif mode=='broom':
  picture('NewBooster_Icon_Clear',20,55,110,110);picture('Tutorial_Hand_1',80,115,60,75)
  picture('WaitingSlots_Reference',155,65,210,60)
  for n,x in [('Hanger_3',180),('Shoes_6',240),('Socks_4',300)]:picture(n,x,65,43,46)
  arrow(395,103);picture('GP_Icon_RainbowBox',500,45,130,120)
  draw.text((270,170),'Clear all waiting items!',font=font,fill='#273D30')
 else:
  picture('GP_Box_Unlock',70,45,145,120);picture('Tutorial_Hand_1',165,110,65,82);arrow(280,103)
  picture('GP_Box0',390,45,145,120)
  draw.text((555,77),'Tap a locked box',font=font,fill='#273D30')
  draw.text((555,112),'to add one more!',font=font,fill='#273D30')
 canvas.save(r/'visuals'/f'Tutorial_{mode}_Reference.png')
print('Saved four tutorial illustrations using game sprites.')
