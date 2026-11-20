import pathlib,json
r=pathlib.Path('analysis');a=json.loads((r/'mono-index.json').read_text(encoding='utf8'))
for x in a:
 if x['class'] in ['HappyTidy.Gameplay.GameplayManager','HappyTidy.Gameplay.UI.PopupBuyBooster','HappyTidy.Gameplay.UI.PopupOutOfLives','AudioDefaultSO','HappyTidy.Gameplay.MapCamera','HappyTidy.Gameplay.UI.GameplayHUD'] or x['name']=='RemoteConfigData':
  d=json.loads((r/'mono'/(x['file']+'_'+str(x['id'])+'.json')).read_text(encoding='utf8'))
  print('###',x['id'],x['class']);print(json.dumps(d,ensure_ascii=False)[:7500])
d=json.loads((r/'mono/resources.assets_10789.json').read_text(encoding='utf8'));print('CONFIG SCALAR',json.dumps({k:v for k,v in d.items() if isinstance(v,(int,float,str))},ensure_ascii=False))
