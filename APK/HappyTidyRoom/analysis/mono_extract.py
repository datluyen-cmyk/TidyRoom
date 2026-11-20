import sys,pathlib,zipfile,json,collections
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom');sys.path.insert(0,str(r/'analysis/vendor'));import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
z=zipfile.ZipFile(r/'puzzle.happy.tidy.room-9-config.arm64_v8a.apk');lib=z.read('lib/arm64-v8a/libil2cpp.so');(r/'analysis/libil2cpp.so').write_bytes(lib)
e=UnityPy.load(str(r/'analysis/data.unity3d'));print('versions',[(f.name,getattr(f,'unity_version',None)) for f in e.files.values()],flush=True)
g=TypeTreeGenerator('6000.0.66f2');g.load_il2cpp(lib,(r/'analysis/global-metadata.dat').read_bytes());print('loaded',flush=True)
out=r/'analysis/mono';out.mkdir(exist_ok=True);records=[];err=[]
for o in e.objects:
 if o.type.name!='MonoBehaviour':continue
 try:
  base=o.read(check_read=False);script=base.m_Script.deref().read();full=(script.m_Namespace+'.' if script.m_Namespace else '')+script.m_ClassName
  nodes=TypeTreeNode.from_list(json.loads(g.get_nodes_as_json(script.m_AssemblyName.removesuffix(".dll"),full)));d=o.read_typetree(nodes);name=d.get('m_Name','');records.append({'id':o.path_id,'name':name,'class':full,'file':o.assets_file.name});(out/(o.assets_file.name+'_'+str(o.path_id)+'.json')).write_text(json.dumps(d,ensure_ascii=False,default=str),encoding='utf8')
 except Exception as ex:err.append(str(ex)[:250])
(r/'analysis/mono-index.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8');print('OK',len(records),'errors',len(err),err[:10]);print('NAMED',[(x['id'],x['name'],x['class']) for x in records if x['name']])



