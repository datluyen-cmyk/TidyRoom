exec(open('analysis/manifest.py',encoding='utf8').read().split("print('CATALOG'")[0] if False else '');import pathlib,struct,json
r=pathlib.Path('analysis');b=(r/'AndroidManifest.xml').read_bytes();ss=json.loads((r/'manifest-strings.json').read_text(encoding='utf8'));p=8
while p<len(b):
 typ,hs,size=struct.unpack_from('<HHI',b,p)
 if typ==258:
  ns,ni,ast,asz,ac,ii,ci,si=struct.unpack_from('<II6H',b,p+16);name=ss[ni];attrs={}
  for j in range(ac):
   q=p+16+ast+j*asz;ans,an,raw,vs,res,vt,val=struct.unpack_from('<IIIHBBI',b,q);attrs[ss[an]]=ss[val] if vt==3 else val
  if name in ['manifest','uses-sdk'] or name=='activity' and 'Unity' in str(attrs):print(name,attrs)
 p+=size
