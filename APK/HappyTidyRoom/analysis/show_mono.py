import pathlib,json
r=pathlib.Path('analysis'); p=r/'mono-index.json'
if p.exists():
 a=json.loads(p.read_text(encoding='utf8'));print('count',len(a));print('\n'.join(str(x) for x in a if x['name'] or any(s in x['class'] for s in ['GameplayConfig','GeneralConfig','BoosterDatabase','GameplayManager','Storage','Queue','BoxController','GameSfx','IdleHint','Configs','Heart'])))
