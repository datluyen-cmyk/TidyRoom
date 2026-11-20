import sys,pathlib,json
r=pathlib.Path('analysis');sys.path.insert(0,str(r/'vendor'));import UnityPy
e=UnityPy.load(str(r/'data.unity3d'));print('files',[(f.name,f.unity_version) for f in e.assets]);n=0
for o in e.objects:
 if o.type.name=='MonoBehaviour':
  d=o.read(check_read=False);s=d.m_Script.deref().read();
  if s.m_AssemblyName=='Assembly-CSharp.dll' or 'HappyTidy' in s.m_Namespace:
   print('SCRIPT',s.m_ClassName,s.m_Namespace,repr(s.m_AssemblyName),'NAME',d.m_Name,'ID',o.path_id,'file',o.assets_file.name);n+=1
   (r/'mono'/(o.assets_file.name+'_'+str(o.path_id)+'.bin')).write_bytes(o.get_raw_data())
  if n>20:break
ls=json.loads((r/'literals.json').read_text(encoding='utf8'));print('GAME HELP', '\n'.join(x for x in ls if any(v in x for v in ['BirdSort','Core tutorial','Booster Clear:','Booster Vacuum','REFILL_HEART_COST','trên','Hộp','hộp','khay','đồ vật','slot','Slot']) and len(x)<1600))

