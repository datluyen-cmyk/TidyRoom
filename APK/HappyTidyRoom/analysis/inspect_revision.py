import pathlib,json,collections
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom\analysis');cat=json.loads((r/'mono/resources.assets_7861.json').read_text(encoding='utf8'));print('CAT KEYS',cat.keys());print('GROUP SAMPLE',cat['groups'][35:43]);print('SUB',cat['subGroups'][330:340]);print('ITEMS',cat['items'][:2]);print('COUNTS',collections.Counter(x['subGroup'] for x in cat['items']).most_common(8))
a=json.loads((r/'unity-index.json').read_text(encoding='utf8'));print('UI SPRITES',[(x['id'],x['name'],x['file']) for x in a if x['type']=='Sprite' and any(k in x['name'].lower() for k in ['booster','vacuum','broom','slot','locked','rainbow','question','frozen','bomb','chain','mystery'])][:100]);
files=list((r/'unity').glob('*level_*.txt')); keys=collections.Counter(); extras=collections.Counter(); diff=collections.Counter();orderkeys=collections.Counter();special=[]
for p in files:
 try:d=json.loads(p.read_text(encoding='utf8'))
 except:continue
 keys.update(d.keys())
 for x in d.get('content',[]):extras.update(x.keys())
 for x in d.get('order',[]):orderkeys.update(x.keys());diff[x.get('diff')]+=1
 for k,v in d.items():
  if k not in ['bgPosX','bg','levelName','order','content','plan']:special.append((p.name,k,str(v)[:200]))
print('LEVEL KEYS',keys,'CONTENT',extras,'ORDERS',orderkeys,'DIFF',diff,'EXTRA',special[:20])
