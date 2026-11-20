import zipfile, pathlib, xml.etree.ElementTree as E, json
root=pathlib.Path(r'D:\APK Works\HappyTidyRoom')
for p in root.glob('*.apk'):
 z=zipfile.ZipFile(p); names=z.namelist(); (root/'analysis'/(p.stem+'-inventory.txt')).write_text('\n'.join(f'{i.file_size}\t{i.filename}' for i in z.infolist()),encoding='utf8')
 print(p.name,len(names));print('\n'.join(names[:65])); print('INTERESTING', '\n'.join(n for n in names if any(x in n.lower() for x in ['metadata','assembly','json','csv','lua','js','level','config','catalog']) )[:12000])
p=pathlib.Path(r'D:\[Rotate Rings] GDD.xlsx');z=zipfile.ZipFile(p); ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
strings=[]
if 'xl/sharedStrings.xml' in z.namelist():
 for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns):strings.append(''.join(t.text or '' for t in si.iter('{'+ns['s']+'}t')))
wb=E.fromstring(z.read('xl/workbook.xml')); print('SHEETS',[(s.attrib) for s in wb.find('s:sheets',ns)])
res=[]
for f in z.namelist():
 if f.startswith('xl/worksheets/sheet') and f.endswith('.xml'):
  lines=[f]
  for row in E.fromstring(z.read(f)).findall('.//s:row',ns):
   cells=[]
   for c in row.findall('s:c',ns):
    v=c.find('s:v',ns); t=c.attrib.get('t'); val=v.text if v is not None else ''
    if t=='s':val=strings[int(val)]
    if t=='inlineStr':val=''.join(x.text or '' for x in c.findall('.//s:t',ns))
    if val:cells.append(c.attrib['r']+': '+val)
   if cells:lines.append(' | '.join(cells))
  res.extend(lines)
(root/'analysis'/'reference-workbook.txt').write_text('\n'.join(res),encoding='utf8');print('\n'.join(res)[:23000])
