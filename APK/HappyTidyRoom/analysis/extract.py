import zipfile,pathlib,re,struct,json
r=pathlib.Path(r'D:\APK Works\HappyTidyRoom');z=zipfile.ZipFile(r/'puzzle.happy.tidy.room-9.apk')
for n in ['assets/bin/Data/Managed/Metadata/global-metadata.dat','assets/bin/Data/ScriptingAssemblies.json','assets/bin/Data/boot.config','assets/bin/Data/data.unity3d','AndroidManifest.xml']:
 p=r/'analysis'/pathlib.Path(n).name;p.write_bytes(z.read(n))
b=(r/'analysis/global-metadata.dat').read_bytes();print('METADATA HEADER',struct.unpack_from('<20I',b));
strs=[x.decode('utf8',errors='replace') for x in re.findall(rb'[\x20-\x7e]{4,}',b)];(r/'analysis/metadata-strings.txt').write_text('\n'.join(strs),encoding='utf8')
print('assemblies', (r/'analysis/ScriptingAssemblies.json').read_text());
print('CUSTOM STRINGS', '\n'.join(s for s in strs if re.search(r'(?i)(booster|revive|tidy|hint|coin|timeup|fail|lose|winpanel|tutorial|combo|freeze|shuffle|sort|closet|room|clean)',s))[-22000:])
