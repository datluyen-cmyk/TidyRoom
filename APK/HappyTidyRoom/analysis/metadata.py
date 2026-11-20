import pathlib,csv,json,struct
r=pathlib.Path('analysis'); b=(r/'global-metadata.dat').read_bytes();a=struct.unpack_from('<64I',b);off,size=a[6:8];s=b[off:off+size].split(b'\0');p=r/'symbols.txt';p.write_text('\n'.join(x.decode('utf8',errors='replace') for x in s),encoding='utf8')
o,c=a[2:4];dataoff,datasize=a[4:6];ls=[]
for i in range(c//8):
 n,idx=struct.unpack_from('<II',b,o+i*8);ls.append(b[dataoff+idx:dataoff+idx+n].decode('utf8',errors='replace'))
(r/'literals.json').write_text(json.dumps(ls,ensure_ascii=False,indent=2),encoding='utf8');print('literals',len(ls));
with open(r/'unity/3175_IngameUI.txt',encoding='utf8') as f:
 rows=list(csv.reader(f));print('\n'.join(' | '.join(x[:2]) for x in rows if x))
