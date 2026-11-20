import pathlib,json
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom\analysis');a=json.loads((r/'mono-index.json').read_text(encoding='utf8'));u=json.loads((r/'unity-index.json').read_text(encoding='utf8'))
for x in a:
 if x['class']=='HappyTidy.Gameplay.Box':
  d=json.loads((r/'mono'/(x['file']+'_'+str(x['id'])+'.json')).read_text(encoding='utf8'));print('BOX',x['id'],json.dumps(d)[:4000])
print('rainbow',[(x['name'],x['type'],x['id']) for x in u if any(k in x['name'].lower() for k in ['rainbow','question','unlock_mechanic','frozen','mystery','hidden','lock','icon_add','slot','box_']) and x['type'] in ['Sprite','GameObject']][:100])
print('MECHANIC', (r/'mono/resources.assets_10791.json').read_text(encoding='utf8'))
