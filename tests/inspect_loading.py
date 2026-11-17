from pathlib import Path
import re
s=Path('index.html').read_text()
print('LENGTH',len(s),'LINES',len(s.splitlines()))
for pat in ['palavras-v','jmdict','palavras-10mil','<script','<body','</body>','id="search"','favorit','dicionário','dicionario','fetch(','DOMContentLoaded','const palavras','let palavras','window.palavras']:
 print('\nPATTERN',pat,'COUNT',s.lower().count(pat.lower()))
 for m in list(re.finditer(re.escape(pat),s,re.I))[:5]:
  print('SNIP',re.sub(r'\s+',' ',s[max(0,m.start()-130):m.end()+160])[:310])
print('\nSCRIPT TAGS')
for m in re.finditer(r'<script[^>]*>',s,re.I):
 print(re.sub(r'\s+',' ',m.group(0))[:300])
