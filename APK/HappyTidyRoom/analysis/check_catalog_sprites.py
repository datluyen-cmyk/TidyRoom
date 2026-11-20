import pathlib,json,collections
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom\analysis');c=json.loads((r/'mono/resources.assets_7861.json').read_text(encoding='utf8'));a=json.loads((r/'unity-index.json').read_text(encoding='utf8'));sprites={x['name'] for x in a if x['type']=='Sprite'};ids={x['id'] for x in c['items']};print('MISSING',len(ids-sprites),sorted(ids-sprites)[:25]);used=set();order=collections.Counter()
for p in (r/'unity').glob('*level_*.txt'):
 try:d=json.loads(p.read_text(encoding='utf8'))
 except:continue
 used.update(x['id'] for x in d.get('content',[]));order.update(x['type'] for x in d.get('order',[]))
print('USED',len(used),'UNKNOWN',len(used-ids),'CATEGORYORDER',len(order));print('MONO BOOSTER', (r/'mono/resources.assets_10900.json').read_text(encoding='utf8'))
