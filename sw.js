// Kotoba v200 (teste): carregamento mais leve e cache de recursos estáticos.
const CACHE = "kotoba-offline-v201-main-20261117";
const CORE = [
  "./index.html", "./pratica.html", "./layout-compartilhado.css",
  "./kanji-dados.js", "./tracos.js",
  "./manifest.webmanifest", "./icones.js",
  "./palavras-v196.js", "./palavras-v197.js",
  "./palavras-v198.js", "./palavras-v199.js"
];
const WORD_SCRIPTS = [196, 197, 198, 199];

self.addEventListener("install", event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // Preservar os recursos essenciais para o modo offline.
    await Promise.allSettled(CORE.map(async path => {
      const response = await fetch(new Request(path, {cache: "reload"}));
      if (response.ok) await cache.put(path, response);
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith("kotoba-offline-") && k !== CACHE)
      .map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

function addWordScripts(html) {
  if (!html.includes("</body>")) return html;
  const missing = WORD_SCRIPTS.filter(version =>
    !html.includes("palavras-v" + version + ".js")
  );
  if (!missing.length) return html;
  const tags = missing.map(version =>
    '<script src="./palavras-v' + version + '.js?v=' + version + '"></script>'
  ).join("");
  return html.replace("</body>", tags + "</body>");
}

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;

  const url = new URL(request.url);
  const isNavigation = request.mode === "navigate";
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    if (isNavigation) {
      let response;
      try {
        response = await fetch(new Request(request, {cache: "no-store"}));
        if (response.ok) event.waitUntil(cache.put(request, response.clone()));
      } catch (_) {}
      if (!response || !response.ok) {
        response = await cache.match(request, {ignoreSearch: true})
          || await cache.match("./index.html");
      }
      if (!response) return Response.error();
      if (url.pathname.endsWith("/") || url.pathname.endsWith("/index.html")) {
        const html = await response.text();
        return new Response(addWordScripts(html), {
          status: 200,
          headers: {"Content-Type": "text/html; charset=utf-8", "Cache-Control": "no-store"}
        });
      }
      return response;
    }

    // Arquivos do dicionario: rede primeiro para nao servir versoes antigas.
    const isDictionaryScript = /\/palavras(?:-extras|-cotidiano|-v|\.)/.test(url.pathname);
    if (isDictionaryScript) {
      try {
        const response = await fetch(new Request(request, {cache: "no-store"}));
        if (response.ok) {
          event.waitUntil(cache.put(request, response.clone()));
          return response;
        }
      } catch (_) {}
      return await cache.match(request) || Response.error();
    }
    const cached = await cache.match(request);
    if (cached) return cached;
    try {
      const response = await fetch(request);
      if (response.ok && response.type === "basic") {
        event.waitUntil(cache.put(request, response.clone()));
      }
      return response;
    } catch (_) {
      return Response.error();
    }
  })());
});
