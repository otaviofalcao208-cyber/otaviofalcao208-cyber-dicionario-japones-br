/* Kotoba: ícones vetoriais locais, sem bibliotecas externas. */
(()=>{"use strict";
const paths={
book:'<path d="M12 7v14m0-14C9 5 5 5 3 6v14c3-1 6-1 9 1m0-14c3-2 7-2 9-1v14c-3-1-6-1-9 1"/>',
brain:'<path d="M12 18V5a3 3 0 0 0-5.8-1A4 4 0 0 0 4 11a4 4 0 0 0 2 7 3 3 0 0 0 6 0Zm0 0V5a3 3 0 0 1 5.8-1A4 4 0 0 1 20 11a4 4 0 0 1-2 7 3 3 0 0 1-6 0Z"/>',
pen:'<path d="m14 5 5 5M4 20l4.5-1 11-11a2.1 2.1 0 0 0-3-3l-11 11L4 20Z"/>',
cloud:'<path d="M7 18h11a4 4 0 0 0 .5-8A7 7 0 0 0 5 12a3 3 0 0 0 2 6Z"/>',
archive:'<rect x="3" y="4" width="18" height="4" rx="1"/><path d="M5 8v12h14V8m-9 4h4"/>',
moon:'<path d="M20 15.5A8 8 0 0 1 8.5 4 8 8 0 1 0 20 15.5Z"/>',
sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>',
search:'<circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/>',
plus:'<path d="M12 5v14M5 12h14"/>',
'book-plus':'<path d="M11 7C8 5 5 5 3 6v14c3-1 6-1 9 1m0-14c2-1.4 4-1.8 6-1.6M12 7v14m6-9v8m-4-4h8"/>',
star:'<path d="m12 2.5 3 6.2 6.8 1-4.9 4.8 1.2 6.8-6.1-3.2-6.1 3.2 1.2-6.8-4.9-4.8 6.8-1Z"/>',
keyboard:'<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M6 9h.01M10 9h.01M14 9h.01M18 9h.01M6 12h.01M10 12h.01M14 12h.01M18 12h.01M7 16h10"/>',
undo:'<path d="M9 14 4 9l5-5M4 9h9a7 7 0 0 1 0 14"/>',
trash:'<path d="M3 6h18M8 6V4h8v2m3 0-1 15H6L5 6m5 4v7m4-7v7"/>',
volume:'<path d="M4 9v6h4l5 4V5L8 9H4Zm12 0a5 5 0 0 1 0 6m2-9a9 9 0 0 1 0 12"/>',
check:'<path d="m4 12 5 5L20 6"/>',
arrow:'<path d="M5 12h14m-6-6 6 6-6 6"/>',
download:'<path d="M12 3v12m-5-5 5 5 5-5M4 17v4h16v-4"/>',
upload:'<path d="M12 21V9m-5 5 5-5 5 5M4 7V3h16v4"/>',
save:'<path d="M4 3h14l3 3v15H3V3h1Zm3 0v7h10V3M7 21v-8h10v8"/>',
shuffle:'<path d="M4 6h3c5 0 5 12 10 12h3m-4-4 4 4-4 4M4 18h3c2 0 3-2 4-4m2-4c1-2 2-4 4-4h3m-4-4 4 4-4 4"/>',
eye:'<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
'eye-off':'<path d="m3 3 18 18M10 5.2A11 11 0 0 1 12 5c6 0 10 7 10 7a15 15 0 0 1-3 3.6M6 6.5C3.5 8.2 2 12 2 12s4 7 10 7a10 10 0 0 0 4-.8"/>',
play:'<path d="m8 5 11 7-11 7V5Z"/>',
refresh:'<path d="M20 7V3l-4 4h4a8 8 0 1 0 2 8"/>',
filter:'<path d="M4 5h16l-6 7v6l-4 2v-8L4 5Z"/>',
info:'<circle cx="12" cy="12" r="10"/><path d="M12 11v6m0-10h.01"/>'
};
const byId={theme:'moon',newWord:'book-plus',searchToggle:'search',handwritingToggle:'pen',japaneseKeyboardToggle:'keyboard',handwritingUndo:'undo',handwritingClear:'trash',handwritingSave:'save',japaneseKeyboardBackspace:'undo',speakStudy:'volume',speak:'volume',random:'shuffle',done:'check',undo:'undo',clear:'trash',guide:'eye',toggleArrows:'eye',stepStroke:'play',allStrokes:'eye',downloadStrokes:'download',nextQuiz:'arrow',reset:'refresh',reverse:'refresh',reveal:'eye',next:'arrow',cancel:'undo',save:'save'};
const byPage={dictionary:'book',study:'brain',writing:'pen',account:'cloud',backup:'archive'};
function svg(name){const markup=paths[name];if(!markup)return null;const node=document.createElementNS('http://www.w3.org/2000/svg','svg');node.setAttribute('viewBox','0 0 24 24');node.setAttribute('width','19');node.setAttribute('height','19');node.setAttribute('fill','none');node.setAttribute('stroke','currentColor');node.setAttribute('stroke-width','1.8');node.setAttribute('stroke-linecap','round');node.setAttribute('stroke-linejoin','round');node.setAttribute('aria-hidden','true');node.classList.add('kotoba-icon');node.innerHTML=markup;return node}
function iconFor(el){if(el.id==='theme')return /claro|sol/i.test(el.textContent||'')?'sun':'moon';if(el.dataset.page)return byPage[el.dataset.page];if(el.dataset.dictTab)return el.dataset.dictTab==='favorites'?'star':'book';if(byId[el.id])return byId[el.id];const t=(el.textContent||'').trim();if(el.id==='theme')return /claro|sol/i.test(t)?'sun':'moon';if(/favorit/i.test(t))return 'star';if(/pesquis|buscar/i.test(t))return 'search';if(/nova palavra/i.test(t))return 'book-plus';if(/salvar|exportar/i.test(t))return 'save';if(/importar|carregar/i.test(t))return 'upload';if(/baixar|download/i.test(t))return 'download';if(/apagar|excluir|limpar/i.test(t))return 'trash';if(/ouvir|áudio/i.test(t))return 'volume';if(/desfazer|voltar/i.test(t))return 'undo';if(/próxim/i.test(t))return 'arrow';if(/revelar|mostrar/i.test(t))return 'eye';if(/reiniciar/i.test(t))return 'refresh';return null}
function decorate(el){if(el.closest('#characters,#quizOptions,#japaneseKeyboard,.handwriting-candidates'))return;const name=iconFor(el);if(!name)return;let icon=el.querySelector(':scope > .kotoba-icon');if(icon){if(icon.dataset.name===name)return;icon.remove()}icon=svg(name);if(!icon)return;icon.dataset.name=name;const first=el.firstChild;if(first&&first.nodeType===3){const cleaned=first.textContent.replace(/^\s*(?:📖|🧠|✍️|☁️|📦|🌙|☀️|🔍|📚|★|☆|🔊|🎲|🗑️?|✓|↶|↗|▶|⌫|＋|\+)\s*/u,'');if(cleaned!==first.textContent)first.textContent=cleaned}el.prepend(icon);el.classList.add('kotoba-icon-button')}
function apply(){document.querySelectorAll('nav button,nav a,button:not(.tile):not(.quiz-option)').forEach(decorate)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();
const observer=new MutationObserver(()=>{document.querySelectorAll('#theme,nav button,nav a,.dictionary-subnav button').forEach(decorate)});
observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true});
})();
