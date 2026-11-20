import json,pathlib,collections
r=pathlib.Path('analysis');a=json.loads((r/'unity-index.json').read_text(encoding='utf8'))
for typ in ['AudioClip','AnimationClip','Texture2D','GameObject']:
 vals=[x['name'] for x in a if x['type']==typ];print(typ, vals if typ in ['AudioClip','AnimationClip'] else vals[:120])
for p in (r/'unity').glob('*level_1.txt'):
 d=json.loads(p.read_text(encoding='utf8'));print('LEVEL KEYS',d.keys());print(str(d)[:3500])
