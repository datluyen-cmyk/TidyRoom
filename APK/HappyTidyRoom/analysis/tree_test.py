import sys,pathlib,json
r=pathlib.Path('analysis');sys.path.insert(0,str(r/'vendor'));from TypeTreeGeneratorAPI import TypeTreeGenerator
g=TypeTreeGenerator('6000.0.66f2');g.load_il2cpp((r/'libil2cpp.so').read_bytes(),(r/'global-metadata.dat').read_bytes())
for a in ['Assembly-CSharp','Assembly-CSharp.dll']:
 for c in ['HappyTidy.Gameplay.GameplayManager','GameplayManager']:
  try:
   n=g.get_nodes_as_json(a,c);print(a,c,n[:600])
  except Exception as ex:print(type(ex),str(ex)[:100])
