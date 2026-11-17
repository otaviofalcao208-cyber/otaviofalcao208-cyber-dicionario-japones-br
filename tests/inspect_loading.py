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

print('\nINITIALIZATION AND NAVIGATION')
for pat in ['const seed=', 'const expandedSeed=', 'let words;', 'function render(', 'function showPage(', 'function navigate(', 'function setPage(', 'render();', 'render()', 'data-page', 'adicionarDezMilPalavras()', 'loadSingleReadingDictionary()', 'addEventListener("click"', 'localStorage.setItem("kotoba_words_v7"']:
 print('===',pat)
 for m in list(re.finditer(re.escape(pat),s,re.I))[:4]:
  print('AT',m.start(),'SNIP',re.sub(r'\\s+',' ',s[max(0,m.start()-220):m.start()+1200])[:1450])
print('\nINLINE SCRIPT SIZES')
for i,m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>',s,re.I|re.S)):
 body=m.group(1); print(i,len(body),body[:130].replace('\\n',' '))

print('RENDER_FULL',s[s.find('function render('):s.find('function render(')+4500].replace('\\n',' '))
print('INIT_WORDS',s[61800:65000].replace('\\n',' '))
for i,m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>',s,re.I|re.S)):
 if i>=4: print('ADDITION',i,'START',m.group(1)[:260].replace('\\n',' '),'END',m.group(1)[-240:].replace('\\n',' '))
