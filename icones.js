/* Google Material Icons (Apache-2.0), offline; demais ícones vetoriais locais. */
(()=>{"use strict";
const paths={
book:'<path d="M12 7v14m0-14C9 5 5 5 3 6v14c3-1 6-1 9 1m0-14c3-2 7-2 9-1v14c-3-1-6-1-9 1"/>',
brain:'<path d="M12 18V5a3 3 0 0 0-5.8-1A4 4 0 0 0 4 11a4 4 0 0 0 2 7 3 3 0 0 0 6 0Zm0 0V5a3 3 0 0 1 5.8-1A4 4 0 0 1 20 11a4 4 0 0 1-2 7 3 3 0 0 1-6 0Z"/>',
pen:'<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>',
cloud:'<path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96z"/>',
archive:'<path d="M20.54 5.23l-1.39-1.68C18.88 3.21 18.47 3 18 3H6c-.47 0-.88.21-1.16.55L3.46 5.23C3.17 5.57 3 6.02 3 6.5V19c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6.5c0-.48-.17-.93-.46-1.27zM12 17.5L6.5 12H10v-2h4v2h3.5L12 17.5zM5.12 5l.81-1h12l.94 1H5.12z"/>',
moon:'<path d="M20 15.5A8 8 0 0 1 8.5 4 8 8 0 1 0 20 15.5Z"/>',
sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.42 1.42m11.3 11.3 1.42 1.42M2 12h2m16 0h2M4.93 19.07l1.42-1.42m11.3-11.3 1.42-1.42"/>',
search:'<path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>',
plus:'<path d="M12 5v14M5 12h14"/>',
'book-plus':'<path d="M11 7C8 5 5 5 3 6v14c3-1 6-1 9 1m0-14c2-1.4 4-1.8 6-1.6M12 7v14m6-9v8m-4-4h8"/>',
star:'<path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>',
keyboard:'<path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/><path d="M0 0h24v24H0zm0 0h24v24H0z" fill="none"/>',
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
function svg(name){const markup=paths[name];if(!markup)return null;const node=document.createElementNS('http://www.w3.org/2000/svg','svg');node.setAttribute('viewBox','0 0 24 24');node.setAttribute('width','19');node.setAttribute('height','19');node.setAttribute('fill','currentColor');node.setAttribute('aria-hidden','true');node.classList.add('kotoba-icon');node.innerHTML=markup;return node}
function iconFor(el){if(el.id==='theme')return /claro|sol/i.test(el.textContent||'')?'sun':'moon';if(el.dataset.page)return byPage[el.dataset.page];if(el.dataset.dictTab)return el.dataset.dictTab==='favorites'?'star':'book';if(byId[el.id])return byId[el.id];const t=(el.textContent||'').trim();if(el.id==='theme')return /claro|sol/i.test(t)?'sun':'moon';if(/favorit/i.test(t))return 'star';if(/pesquis|buscar/i.test(t))return 'search';if(/nova palavra/i.test(t))return 'book-plus';if(/salvar|exportar/i.test(t))return 'save';if(/importar|carregar/i.test(t))return 'upload';if(/baixar|download/i.test(t))return 'download';if(/apagar|excluir|limpar/i.test(t))return 'trash';if(/ouvir|áudio/i.test(t))return 'volume';if(/desfazer|voltar/i.test(t))return 'undo';if(/próxim/i.test(t))return 'arrow';if(/revelar|mostrar/i.test(t))return 'eye';if(/reiniciar/i.test(t))return 'refresh';return null}
function decorate(el){if(el.closest('#characters,#quizOptions,#japaneseKeyboard,.handwriting-candidates'))return;const name=iconFor(el);if(!name)return;let icon=el.querySelector(':scope > .kotoba-icon');if(icon){if(icon.dataset.name===name)return;icon.remove()}icon=svg(name);if(!icon)return;icon.dataset.name=name;const first=el.firstChild;if(first&&first.nodeType===3){const cleaned=first.textContent.replace(/^\s*(?:📖|🧠|✍️|☁️|📦|🌙|☀️|🔍|📚|★|☆|🔊|🎲|🗑️?|✓|↶|↗|▶|⌫|＋|\+)\s*/u,'');if(cleaned!==first.textContent)first.textContent=cleaned}el.prepend(icon);el.classList.add('kotoba-icon-button')}
function apply(){document.querySelectorAll('nav button,nav a,button:not(.tile):not(.quiz-option)').forEach(decorate)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();
const observer=new MutationObserver(()=>{document.querySelectorAll('#theme,nav button,nav a,.dictionary-subnav button').forEach(decorate)});
observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true});
})();
