import pathlib,json,collections
r=pathlib.Path('analysis');a=json.loads((r/'mono-index.json').read_text(encoding='utf8'));c=collections.Counter(x['class'] for x in a);print('\n'.join(str((k,v)) for k,v in c.items() if not k.startswith(('TMPro','Unity','Spine','Coffee','DG','HappyTidy.CatalogSpriteRef'))))
for x in a:
 if any(k in x['class'].lower() for k in ['databucket','datawrapper','shop','settingmanager','haptic']):
  d=json.loads((r/'mono'/(x['file']+'_'+str(x['id'])+'.json')).read_text(encoding='utf8')); print('##',x['class'],x['file'],x['id']);print(json.dumps(d,ensure_ascii=False)[:2500])
