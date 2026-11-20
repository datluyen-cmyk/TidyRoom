from pathlib import Path
from PIL import Image
r=Path(r'D:\APK Works\HappyTidyRoom\analysis');a=Image.open(r/'visuals/AddSlot_Img.png').convert('RGBA');b=Image.open(r/'visuals/GP_Slot_Unlock.png').convert('RGBA');a.thumbnail((165,50));b.thumbnail((70,70));im=Image.new('RGBA',(170,145),(255,255,255,0));im.alpha_composite(a,((170-a.width)//2,5));im.alpha_composite(b,((170-b.width)//2,68));im.save(r/'visuals/ExtraSlot_Reference.png')
p=r/'build_original_format.mjs';s=p.read_text(encoding='utf8');s=s.replace("await imageAt(sh,'AddSlot_Img',4,6,165,50);\nawait imageAt(sh,'GP_Slot_Unlock',4,6,70,70);", "await imageAt(sh,'ExtraSlot_Reference',4,6,170,145);");p.write_text(s,encoding='utf8')
