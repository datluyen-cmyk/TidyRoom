"""Compress generated runtime levels. Human-readable Happy exports remain in Converted/."""
from pathlib import Path
import gzip,json
root=Path(__file__).resolve().parents[1]/'Assets/StreamingAssets/TidyRoom'
index=json.loads((root/'index.json').read_text(encoding='utf8'));before=after=count=0
for entry in index['levels']:
    path=root/entry['file']
    if path.suffix=='.gz':continue
    raw=path.read_bytes();packed=gzip.compress(raw,compresslevel=6,mtime=0)
    assert gzip.decompress(packed)==raw
    target=path.with_suffix(path.suffix+'.gz');target.write_bytes(packed)
    path.unlink();entry['file']=str(target.relative_to(root)).replace('\\','/')
    count+=1;before+=len(raw);after+=len(packed)
(root/'index.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf8')
print(f'Packed {count} levels: {before/1e6:.1f} MB -> {after/1e6:.1f} MB')
