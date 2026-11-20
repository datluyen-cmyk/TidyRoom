import pathlib,json
r=pathlib.Path('analysis');a=json.loads((r/'mono-index.json').read_text(encoding='utf8')); classes=['HappyTidy.Gameplay.GameplayManager','HappyTidy.Gameplay.Queue','HappyTidy.Gameplay.Storage','HappyTidy.Gameplay.BoxController','HappyTidy.Gameplay.Board','HappyTidy.Gameplay.GameSfx','HappyTidy.Gameplay.Tutorial.GameplayTutorialController','HappyTidy.Gameplay.UI.PopupRevive','HappyTidy.Gameplay.UI.WinPopup','HeartSystemManager','_Game.Scripts.HeartSystemManager','HappyTidy.Gameplay.UI.GameplayWarningUI','HappyTidy.Gameplay.IdleHint']
for x in a:
 if x['class'] in classes or x['name'] in ['GeneralConfig','GameplayConfig','BoosterDatabase','MechanicDatabase','RemoteConfigData','Reward Catalog SO']:
  d=json.loads((r/'mono'/(x['file']+'_'+str(x['id'])+'.json')).read_text(encoding='utf8'));print('\n###',x['file'],x['id'],x['class'],x['name']);print(json.dumps(d,ensure_ascii=False,indent=1)[:16000])
