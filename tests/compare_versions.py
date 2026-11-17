import asyncio, json, pathlib, statistics, subprocess, time
from playwright.async_api import async_playwright

OUT=pathlib.Path("test-results");OUT.mkdir(exist_ok=True)
report={"versions":{},"checks":{},"limitations":[]}
async def evaluate_version(browser, label, port):
    server=subprocess.Popen(["python3","-m","http.server",str(port),"--bind","127.0.0.1","--directory", "." if label=="v200" else "/tmp/kotoba-v199"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        for device,viewport,mobile in [("desktop",{"width":1366,"height":768},False),("mobile",{"width":390,"height":844},True)]:
            key=label+"_"+device
            samples=[];errors=[];details={}
            for i in range(3):
                context=await browser.new_context(viewport=viewport,is_mobile=mobile,has_touch=mobile,service_workers="allow")
                page=await context.new_page()
                page.on("pageerror",lambda e:errors.append(str(e)))
                start=time.monotonic()
                response=await page.goto(f"http://127.0.0.1:{port}/index.html",wait_until="domcontentloaded",timeout=90000)
                elapsed=round((time.monotonic()-start)*1000)
                samples.append(elapsed)
                if i==0:
                    details["http_status"]=response.status if response else None
                    details["title"]=await page.title()
                    details["controls"]=await page.locator("input,button").count()
                    inputs=page.locator('input[type="search"],input[type="text"],input:not([type])')
                    details["text_inputs"]=await inputs.count()
                    details["speech_synthesis_available"]=await page.evaluate("typeof speechSynthesis !== 'undefined'")
                    details["audio_elements"]=await page.locator("audio").count()
                    details["favorite_controls"]=await page.locator('[aria-label*="favorit" i],[title*="favorit" i],button:has-text("Favorit")').count()
                    if await inputs.count():
                        try:
                            target=inputs.first
                            await target.fill("こんにちは",timeout=5000)
                            details["japanese_text_accepted"]=(await target.input_value())=="こんにちは"
                            details["search_event_dispatched"]=await target.evaluate("(el)=>{el.dispatchEvent(new Event('input',{bubbles:true}));return true}")
                        except Exception as exc:
                            details["search_error"]=str(exc)[:300]
                    await page.screenshot(path=str(OUT/(key+".png")),full_page=False)
                    await page.wait_for_timeout(2500)
                    details["sw_registration"]=await page.evaluate("async()=> (await navigator.serviceWorker.getRegistrations()).length")
                    # Testa apenas carregamento offline com cache aquecido, não todo o conteúdo.
                    try:
                        await page.reload(wait_until="domcontentloaded",timeout=20000)
                        await page.wait_for_timeout(1500)
                        await context.set_offline(True)
                        offline=await page.reload(wait_until="domcontentloaded",timeout=12000)
                        details["offline_reload"]=bool(offline and offline.status==200 and await page.locator("body").is_visible())
                    except Exception as exc:
                        details["offline_reload"]=False
                        details["offline_error"]=str(exc)[:250]
                await context.close()
            details["domcontentloaded_ms"]=samples
            details["median_domcontentloaded_ms"]=statistics.median(samples)
            details["page_errors"]=errors[:10]
            report["versions"][key]=details
            print(key,json.dumps(details,ensure_ascii=False),flush=True)
    finally:
        server.terminate()
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(headless=True,args=["--no-sandbox"])
        await evaluate_version(browser,"v199",8766)
        await evaluate_version(browser,"v200",8767)
        await browser.close()
    for device in ("desktop","mobile"):
        old=report["versions"]["v199_"+device]["median_domcontentloaded_ms"]
        new=report["versions"]["v200_"+device]["median_domcontentloaded_ms"]
        report["checks"][device+"_v200_vs_v199_pct"]=round((new-old)/old*100,1) if old else None
    report["limitations"]=[
      "A medição usa DOMContentLoaded, não mede interatividade completa nem rede móvel real.",
      "Pesquisa: preenchimento e evento de entrada; resultados de dicionário não são validados semanticamente.",
      "Favoritos: presença de controles; persistência não confirmada sem seletores estáveis.",
      "Áudio: disponibilidade da API; reprodução sonora não confirmada.",
      "Offline: somente recarga da página após aquecimento de cache."
    ]
    (OUT/"comparison.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report["checks"],ensure_ascii=False),flush=True)
asyncio.run(main())
