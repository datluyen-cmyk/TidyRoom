import json, zipfile, posixpath, xml.etree.ElementTree as E
from pathlib import Path
root=Path(r'D:\APK Works\HappyTidyRoom')
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read(p):
 z=zipfile.ZipFile(p)
 strings=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 rels={r.attrib['Id']:r.attrib['Target'] for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 out={}
 for s in E.fromstring(z.read('xl/workbook.xml')).find('s:sheets',ns):
  target=rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
  file=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
  xml=E.fromstring(z.read(file)); cells={}
  for c in xml.findall('.//s:sheetData/s:row/s:c',ns):
   v=c.find('s:v',ns); value=v.text if v is not None else ''
   if c.attrib.get('t')=='s': value=strings[int(value)]
   elif c.attrib.get('t')=='inlineStr': value=''.join(c.find('s:is',ns).itertext())
   assert c.attrib.get('t')!='e',(s.attrib['name'],c.attrib['r'],value)
   f=c.find('s:f',ns)
   cells[c.attrib['r']]=(value, f.text if f is not None else None)
  out[s.attrib['name']]=cells
 return out,z
new,z=read(root/'outputs/happy-tidy-room-gdd/Happy Tidy Room - GDD.xlsx')
old,_=read(root/'analysis/before-box-category-revision.xlsx')
assert 'Category Object' in new and not any('Score' in n for n in new)
assert not any(v[0] in ['Phạm vi','Xác minh'] for v in new['Overview'].values())
inv=json.loads((root/'analysis/category-object.json').read_text(encoding='utf-8'))
c=new['Category Object']
expected={}
for x in inv['categories']:
 e=expected.setdefault(x['category'],{'count':0,'used':0,'ids':[]})
 e['count']+=x['count'];e['used']+=x['used'];e['ids'].append(x['id'])
assert len(expected)==355
seen=set()
for row in range(5,360):
 name=c[f'B{row}'][0]; seen.add(name);e=expected[name]
 assert int(c[f'D{row}'][0])==e['count']
 assert int(c[f'F{row}'][0])==e['used']
 assert c[f'G{row}'][0]==', '.join(map(str,e['ids']))
assert seen==expected.keys()
assert c['D360']==('2863','SUM(D5:D359)'),c['D360']
assert c['F360']==('2638','SUM(F5:F359)'),c['F360']
for name in new.keys()-{'Category Object','Overview','Gameplay','Tutorial'}:
 assert new[name]==old[name],name
for index,expected in [(1,6),(2,2),(3,4),(4,355),(5,4)]:
 p=f'xl/drawings/drawing{index}.xml'
 xml=E.fromstring(z.read(p))
 assert len(xml.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing}pic'))==expected
xml=E.fromstring(z.read('xl/worksheets/sheet7.xml'))
for m in xml.findall('s:mergeCells/s:mergeCell',ns):
 ref=m.attrib['ref']
 if ref.startswith('C'):
  first,last=ref.split(':');assert int(last[1:])-int(first[1:])+1<=10
  assert c[first][0]
for name in ['Overview','Gameplay']:
 text=' '.join(v[0] for v in new[name].values())
 for term in ['APK','maxRevives','versionCode','prefab','API 24']:
  assert term not in text,(name,term)
print('PASS: category counts and totals preserved; context merges max 10 rows with repeated labels; Overview and Gameplay simplified; no error cells; unaffected sheet values preserved.')
side=root/'outputs/happy-tidy-room-gdd/Happy Tidy Room - GDD.xlsx.inspect.ndjson'
if side.exists(): side.replace(root/'analysis/revision-inspect.ndjson')
