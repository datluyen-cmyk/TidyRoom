from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'D:/APK Works/HappyTidyRoom/analysis');sys.path.insert(0,str(root/'vendor'))
import UnityPy
dest=Path(__file__).resolve().parents[1]/'Assets/StreamingAssets/TidyRoom/Art'
names={'GP_Box0','GP_Box_0_Front','GP_Box_Unlock','GP_Slot','GP_Frame_Slot','GP_Icon_RainbowBox','GP_Icon_RainbowBox_Front','NewBooster_Icon_Vaccum','NewBooster_Icon_Clear'}
e=UnityPy.load(str(root/'data.unity3d'));count=0
for o in e.objects:
    if o.type.name!='Sprite':continue
    d=o.read();n=d.m_Name
    if n.startswith('HT_BG_') or n in names:
        isbg=n.startswith('HT_BG_');out=dest/('HappyBG' if isbg else 'UI')/(n+('.jpg' if isbg else '.png'));out.parent.mkdir(parents=True,exist_ok=True)
        if not out.exists():
            if isbg:d.image.convert('RGB').save(out,quality=95,subsampling=0)
            else:d.image.save(out)
        old=out.with_suffix('.png')
        if isbg and old.exists():old.unlink()
        count+=1
print('Exported backgrounds/UI:',count)
