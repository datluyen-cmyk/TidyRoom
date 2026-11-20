import pathlib,json,re
r=pathlib.Path('analysis');ls=json.loads((r/'literals.json').read_text(encoding='utf8')); out=[]
for i,s in enumerate(ls):
 if re.search(r'(HappyTidy|Booster Clear|Booster Vacuum|BirdSort|queue|Queue|Storage|storage|box |Box |revive|Revive|REFILL_HEART_COST|Core tutorial|Đi|Nếu|tim|hộp|coin|Coin|Coins)',s):
  if len(s)<2200:out.append(f'{i}: {s}')
(r/'game-literals.txt').write_text('\n'.join(out),encoding='utf8');print('\n'.join(out)[-16000:])
