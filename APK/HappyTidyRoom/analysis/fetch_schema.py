import urllib.request,pathlib
u='https://raw.githubusercontent.com/Perfare/Il2CppDumper/master/Il2CppDumper/Il2Cpp/MetadataClass.cs'
p=pathlib.Path('analysis/MetadataClass.cs');p.write_bytes(urllib.request.urlopen(u).read())
