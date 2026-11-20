import pathlib,json,struct,hashlib
r=pathlib.Path('analysis');d=json.loads((r/'mono/resources.assets_7861.json').read_text(encoding='utf8'));print('CATALOG',[(k,len(v) if isinstance(v,list) else type(v).__name__) for k,v in d.items()]);print('SUBGROUP SAMPLE',str(d.get('subGroups',d.get('subgroups',[])))[:1400]);print('ITEM',str(d.get('items',[]))[:700]);
b=(r/'AndroidManifest.xml').read_bytes();p=8
while p<len(b):
 typ,hs,size=struct.unpack_from('<HHI',b,p)
 if typ==1:
  cnt,styles,flags,start,ststart=struct.unpack_from('<IIIII',b,p+8);ss=[]
  for i in range(cnt):
   off=struct.unpack_from('<I',b,p+hs+i*4)[0];q=p+start+off
   if flags&256:
    n=b[q];q+=1
    if n&128:q+=1
    n=b[q];q+=1
    if n&128:n=((n&127)<<8)|b[q];q+=1
    ss.append(b[q:q+n].decode('utf8',errors='replace'))
   else:
    n=struct.unpack_from('<H',b,q)[0];q+=2;ss.append(b[q:q+n*2].decode('utf16',errors='replace'))
  (r/'manifest-strings.json').write_text(json.dumps(ss,ensure_ascii=False,indent=2),encoding='utf8');print('MANIFEST STR', [s for s in ss if any(k in s.lower() for k in ['happy','version','portrait','landscape']) or s[:1].isdigit()][:35])
 p+=size
