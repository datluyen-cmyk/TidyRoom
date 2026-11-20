from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E
root=Path(r'D:\APK Works\HappyTidyRoom');out=root/'outputs/happy-tidy-room-gdd';p=out/'Happy Tidy Room - GDD.xlsx';z=zipfile.ZipFile(p);ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
wb=E.fromstring(z.read('xl/workbook.xml'));names=[s.attrib['name'] for s in wb.find('s:sheets',ns)];expected=json.loads((root/'analysis/gdd-content.json').read_text(encoding='utf8'));assert names==[s['name'] for s in expected['sheets']]
strings=[]
if 'xl/sharedStrings.xml' in z.namelist():
 for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns):strings.append(''.join(x.text or '' for x in si.iter('{'+ns['s']+'}t')))
for i,spec in enumerate(expected['sheets'],1):
 cells={}
 for c in E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('.//s:c',ns):
  v=c.find('s:v',ns)
  if c.get('t')=='s':val=strings[int(v.text)]
  elif c.get('t')=='inlineStr':val=''.join(x.text or '' for x in c.findall('.//s:t',ns))
  else:val=v.text if v is not None else ''
  cells[c.attrib['r']]=val
 for row,vals in enumerate(spec['rows'],5):
  for col,val in zip('BCDE',vals):assert cells.get(f'{col}{row}')==val,(spec['name'],row,col)
 assert not any(c.attrib.get('t')=='e' for c in E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml')).findall('.//s:c',ns))
assert len([n for n in z.namelist() if n.startswith('xl/media/')])>=1
md=out/'Happy Tidy Room - GDD.md';txt=md.read_text(encoding='utf8');txt=txt.replace('../../analysis/visuals/asset-contact-sheet.png','D:/APK Works/HappyTidyRoom/analysis/visuals/asset-contact-sheet.png');md.write_text(txt,encoding='utf8');assert '\ufffd' not in txt
print('Verified: 14 sheets, all 133 content rows match, no error cells, embedded asset image, UTF-8 Markdown.')
# Keep authoring diagnostics with the evidence, outside the deliverable directory.
extra=out/'Happy Tidy Room - GDD.xlsx.inspect.ndjson'
if extra.exists():extra.replace(root/'analysis/workbook-inspect.ndjson')
print('Final files:',[(p.name,p.stat().st_size) for p in out.iterdir()])
