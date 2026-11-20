import zipfile,xml.etree.ElementTree as E
z=zipfile.ZipFile(r'D:\[Rotate Rings] GDD.xlsx');ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for i in range(1,14):
 t=E.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'));print('SHEET',i,'cols', [x.attrib for x in t.findall('s:cols/s:col',ns)],'merge',[x.attrib for x in t.findall('s:mergeCells/s:mergeCell',ns)],'rows', [x.attrib for x in t.findall('s:sheetData/s:row',ns)[:6]])
