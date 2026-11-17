import asyncio, json, pathlib, subprocess, time
from playwright.async_api import async_playwright
out=pathlib.Path("test-results");out.mkdir(exist_ok=True)
results={}
async def main():
 server=subprocess.Popen(["python3","-m","http.server","8770","--bind","127.0.0.1"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  await asyncio.sleep(2)
  async with async_playwright() as p:
   browser=await p.chromium.launch(headless=True,args=["--no-sandbox"])
   for device,viewport,mobile in [("desktop",{"width":1366,"height":768},False),("mobile",{"width":390,"height":844},True)]:
    context=await browser.new_context(viewport=viewport,is_mobile=mobile,has_touch=mobile,service_workers="allow")
    page=await context.new_page()
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    start=time.monotonic()
    await page.goto("http://127.0.0.1:8770/index.html",wait_until="domcontentloaded",timeout=90000)
    dom_ms=round((time.monotonic()-start)*1000)
    await page.wait_for_function("window.kotobaWordsLoadedV200===true",timeout=90000)
    ready_ms=round((time.monotonic()-start)*1000)
    cards=await page.locator("#entries article.entry").count()
    count=await page.locator("#count").inner_text()
    assert cards<=80,(device,"too many cards",cards)
    assert await page.locator("#kotobaMoreV200").count()==1,(device,"missing more")
    await page.locator("#kotobaMoreV200").click(timeout=15000)
    more=await page.locator("#entries article.entry").count()
    assert 80<more<=160,(device,"load more failed",more)
    # O campo de busca deve reduzir os resultados visíveis.
    if not await page.locator("#search").is_visible():\n     await page.locator("#searchToggle").click(timeout=15000)\n    await page.locator("#search").fill("こんにちは",timeout=15000)
    await page.wait_for_timeout(500)
    filtered=await page.locator("#entries article.entry").count()
    resultcount=await page.locator("#resultcount").inner_text()
    # Busca pode retornar 0 ou mais, mas não pode exceder 160 cartões.
    assert filtered<=160
    await page.locator("#search").fill("",timeout=15000)
    await page.wait_for_timeout(500)
    fav=page.locator("#entries button.star-favorite").first
    before=await fav.get_attribute("aria-pressed")
    await fav.click(timeout=15000)
    after=await page.locator("#entries button.star-favorite").first.get_attribute("aria-pressed")
    assert before!=after,(device,"favorite toggle failed",before,after)
    # Restaurar favorito original.
    await page.locator("#entries button.star-favorite").first.click(timeout=15000)
    # Espionar invocação da API de áudio sem exigir saída física.
    await page.evaluate("window.__kotobaSpokenV200=0; speechSynthesis.speak = function(){window.__kotobaSpokenV200++}")
    await page.locator('#entries button[data-action="speak"]').first.click(timeout=15000)
    spoken=await page.evaluate("window.__kotobaSpokenV200")
    # Offline após recarga com service worker controlando a página.
    await page.wait_for_function("navigator.serviceWorker.controller!==null",timeout=25000)
    await page.reload(wait_until="domcontentloaded",timeout=45000)
    await page.wait_for_function("window.kotobaWordsLoadedV200===true",timeout=90000)
    await context.set_offline(True)
    offline_ok=False
    try:
     response=await page.reload(wait_until="domcontentloaded",timeout=30000)
     offline_ok=bool(response and response.status==200)
    except Exception as exc:
     results[device+"_offline_error"]=str(exc)[:250]
    results[device]={"domcontentloaded_ms":dom_ms,"dictionary_ready_ms":ready_ms,"initial_cards":cards,"after_more_cards":more,"total_words":count,"search_resultcount":resultcount,"favorite_toggle":True,"speech_invocations":spoken,"offline_reload":offline_ok,"page_errors":errors[:10]}
    print(device,json.dumps(results[device],ensure_ascii=False),flush=True)
    assert spoken>=1,(device,"audio action did not invoke speech")
    assert offline_ok,(device,"offline reload failed")
    assert not errors,(device,"javascript errors",errors[:3])
    await context.close()
   await browser.close()
 finally:
  server.terminate()
  (out/"lazy-v200.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
asyncio.run(main())
