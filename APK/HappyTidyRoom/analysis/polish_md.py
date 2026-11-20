from pathlib import Path
p=Path('analysis/write_gdd.py');s=p.read_text(encoding='utf8');s=s.replace("md += [f'### {label}', '', body, '', f'*Xác minh: {status}. Nguồn: {src}.*', '']", "md += [f'### {label}', '', body, '']")
s=s.replace("md += [f'## {idx+1}. {sh[\"title\"]}', '']", "md += [f'## {idx+1}. {sh[\"title\"]}', '']\n    if sh['name'] != 'Nguồn & Xác minh':\n        refs = sorted({part.strip() for row in sh['rows'] for part in row[3].split(',')})\n        md += ['*Nguồn đối chiếu: ' + ', '.join(refs) + '. Xem mục Nguồn và giới hạn xác minh.*', '']")
p.write_text(s,encoding='utf8')
