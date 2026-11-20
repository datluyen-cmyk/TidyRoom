import pathlib,struct,json
r=pathlib.Path('analysis');b=(r/'global-metadata.dat').read_bytes();h=struct.unpack_from('<64I',b)
def s(i):
 p=h[6]+i;return b[p:b.index(0,p)].decode('utf8',errors='replace')
def defaults():
 return {idx:(typ,di) for idx,typ,di in struct.iter_unpack('<iii',b[h[16]:h[16]+h[17]])}
def cu(p):
 x=b[p]
 if x<128:return x
 if x<192:return ((x&63)<<8)|b[p+1]
 if x<224:return ((x&31)<<24)|(b[p+1]<<16)|(b[p+2]<<8)|b[p+3]
 if x==240:return struct.unpack_from('<I',b,p+1)[0]
 if x==255:return 0xffffffff
 return 0xfffffffe
def ci(p):
 x=cu(p);return -(x>>1)-1 if x&1 else x>>1
fd=defaults();out=[]
# v31 type definitions 88 bytes
for i in range(h[41]//88):
 t=struct.unpack_from('<16i8H2I',b,h[40]+i*88);name=s(t[0]);ns=s(t[1]);fs=t[8];ms=t[9];fc=t[18];mc=t[16]
 if name in ['Configs','HeartSystemManager','BoosterManager','GameSfx','GameplayManager','BlockRule','Queue','Storage','Box','IdleHint','LevelResolver','BoosterType']:
  lines=[f'### {ns}.{name} fields {fc} methods {mc}']
  for j in range(fc):
   ni,ty,tok=struct.unpack_from('<IiI',b,h[24]+(fs+j)*12);n=s(ni);v=''
   if fs+j in fd:
    dt,di=fd[fs+j];p=h[18]+di;v=f' type={dt} data={di} hex={b[p:p+8].hex()} compressedInt={ci(p)} float32={struct.unpack_from("<f",b,p)[0]}'
   lines.append(n+v)
  lines.append('METHODS '+', '.join(s(struct.unpack_from('<I',b,h[12]+(ms+j)*36)[0]) for j in range(mc)))
  out.extend(lines)
(r/'metadata-game-classes.txt').write_text('\n'.join(out),encoding='utf8');print('\n'.join(out))
