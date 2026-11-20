import pathlib,json
r=pathlib.Path('analysis');a=json.loads((r/'mono-index.json').read_text(encoding='utf8'))
for x in a:
 if x['name'] in ['GeneralConfig','GameplayConfig','BoosterDatabase','MechanicDatabase'] or x['class'] in ['HappyTidy.Gameplay.BoxController','HappyTidy.Gameplay.Storage','HappyTidy.Gameplay.Board','HappyTidy.Gameplay.GameSfx','HappyTidy.Gameplay.Tutorial.GameplayTutorialController','HappyTidy.Gameplay.UI.PopupRevive','HappyTidy.Gameplay.UI.WinPopup','HappyTidy.Gameplay.IdleHint']:
  d=json.loads((r/'mono'/(x['file']+'_'+str(x['id'])+'.json')).read_text(encoding='utf8'));print('###',x['file'],x['id'],x['class'],x['name']);print(json.dumps(d,ensure_ascii=False,indent=1)[:15000])
