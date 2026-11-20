import sys,pathlib,json,collections
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom');sys.path.insert(0,str(r/'analysis/vendor'));import UnityPy
e=UnityPy.load(str(r/'analysis/data.unity3d')); out=r/'analysis/unity';out.mkdir(exist_ok=True); records=[]; errors=[]
for o in e.objects:
 try:
  if o.type.name in ['TextAsset','MonoBehaviour','GameObject','AudioClip','Sprite','Texture2D','AnimationClip','MonoScript']:
   d=o.read_typetree(); name=d.get('m_Name',''); rec={'id':o.path_id,'type':o.type.name,'name':name,'file':o.assets_file.name};records.append(rec)
   if o.type.name=='TextAsset':
    p=out/(str(o.path_id)+'_'+name.replace('/','_').replace('\\','_')+'.txt');p.write_text(str(d.get('m_Script','')),encoding='utf8',errors='replace')
   elif o.type.name in ['MonoBehaviour','MonoScript']:
    (out/(str(o.path_id)+'.json')).write_text(json.dumps(d,ensure_ascii=False,default=str),encoding='utf8')
 except Exception as ex:errors.append(str(ex)[:100])
(r/'analysis/unity-index.json').write_text(json.dumps(records,ensure_ascii=False),encoding='utf8');print(collections.Counter(x['type'] for x in records));print('ERRORS',len(errors),errors[:4]);print('TEXT',[(x['id'],x['name']) for x in records if x['type']=='TextAsset'][:100]);print('MONO',[(x['id'],x['name']) for x in records if x['type']=='MonoBehaviour' and x['name']][:100])
