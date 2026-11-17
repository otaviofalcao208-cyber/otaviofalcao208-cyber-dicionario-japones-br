from pathlib import Path
import re

index=Path("index.html")
html=index.read_text(encoding="utf-8")
if "kotobaLoadWordsV200" in html:
    raise SystemExit("Ja aplicado; nao repetir")
scripts=list(re.finditer(r'<script(?:\\s[^>]*)?>(.*?)</script>',html,re.I|re.S))
assert len(scripts)==19, f"Quantidade inesperada de scripts inline: {len(scripts)}"
# Os blocos finais contêm acréscimos de palavras e ajustes associados.
# Mantê-los juntos preserva a ordem original de execução.
chosen=scripts[3:] # scripts inline 0..2 permanecem; scripts 3..18 migram
assert len(chosen)==16
payload="\n".join(m.group(1) for m in chosen)
assert len(payload)>250000, "Dados extraidos inesperadamente pequenos"
Path("palavras-extras-v200.js").write_text(
    "/* Kotoba v200: dados e ajustes do dicionario carregados sob demanda. */\n"+payload+"\n",
    encoding="utf-8")
for m in reversed(chosen):
    html=html[:m.start()]+html[m.end():]
old='list.length?list.map(w=>'
new='list.length?list.slice(0,window.kotobaVisibleLimitV200||80).map(w=>'
assert html.count(old)==1, "Renderizador nao encontrado"
html=html.replace(old,new,1)
# Preservar acesso a todos os resultados sem construir milhares de cartoes de uma vez.
anchor='renderFlash();renderSingleReadingResults()}'
assert html.count(anchor)==1
html=html.replace(anchor,'''if(list.length>(window.kotobaVisibleLimitV200||80)){
 const more=document.createElement("button");
 more.type="button";more.id="kotobaMoreV200";
 more.textContent="Mostrar mais palavras ("+Math.min(list.length-(window.kotobaVisibleLimitV200||80),80)+")";
 more.onclick=()=>{window.kotobaVisibleLimitV200=(window.kotobaVisibleLimitV200||80)+80;render()};
 $("entries").appendChild(more);
}renderFlash();renderSingleReadingResults()}''',1)
# Sempre reiniciar paginação ao mudar a busca/filtros.
bootstrap='''<script id="kotoba-lazy-words-v200">
(function(){
  let loading;
  window.kotobaLoadWordsV200=function(){
    if(loading)return loading;
    loading=new Promise(function(resolve,reject){
      const script=document.createElement("script");
      script.src="./palavras-extras-v200.js?v=200";
      script.onload=function(){window.kotobaWordsLoadedV200=true;resolve(true)};
      script.onerror=function(){loading=null;reject(new Error("Falha ao carregar palavras extras"))};
      document.body.appendChild(script);
    });
    return loading;
  };
  function maybeLoad(){
    const page=location.hash.slice(1)||"dictionary";
    if(page==="dictionary"||page==="study"){
      window.kotobaLoadWordsV200().catch(console.error);
    }
  }
  window.addEventListener("hashchange",maybeLoad);
  window.addEventListener("popstate",maybeLoad);
  if(document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded",maybeLoad,{once:true});
  }else{setTimeout(maybeLoad,0)}
})();
</script>'''
assert '</body>' in html
html=html.replace('</body>',bootstrap+'\n</body>',1)
index.write_text(html,encoding="utf-8")
print("EXTRACTED_BYTES",len(payload.encode()))
print("INDEX_BYTES",len(html.encode()))
print("EXTRACTED_SCRIPTS",len(chosen))
