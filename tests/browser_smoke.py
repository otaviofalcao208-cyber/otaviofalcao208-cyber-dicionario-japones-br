import asyncio, json, os, pathlib, subprocess, time
from playwright.async_api import async_playwright

OUT = pathlib.Path("test-results")
OUT.mkdir(exist_ok=True)
results = {"checks": {}, "errors": [], "warnings": [], "metrics": {}}
def check(name, condition):
    results["checks"][name] = bool(condition)
    print(("PASS" if condition else "FAIL") + ": " + name, flush=True)

async def main():
    server = subprocess.Popen(["python3", "-m", "http.server", "8765", "--bind", "127.0.0.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        await asyncio.sleep(2)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
            for device, viewport, mobile in [("desktop", {"width": 1366, "height": 768}, False), ("mobile", {"width": 390, "height": 844}, True)]:
                context = await browser.new_context(viewport=viewport, is_mobile=mobile, has_touch=mobile, service_workers="allow", ignore_https_errors=True)
                page = await context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                start = time.monotonic()
                response = await page.goto("http://127.0.0.1:8765/index.html", wait_until="domcontentloaded", timeout=90000)
                elapsed = round((time.monotonic() - start) * 1000)
                results["metrics"][device+"_domcontentloaded_ms"] = elapsed
                check(device+"_html_status", response is not None and response.status == 200)
                check(device+"_body_visible", await page.locator("body").is_visible())
                await page.wait_for_timeout(6000)
                results["metrics"][device+"_title"] = await page.title()
                results["metrics"][device+"_input_count"] = await page.locator("input").count()
                results["metrics"][device+"_button_count"] = await page.locator("button").count()
                results["metrics"][device+"_scripts"] = await page.locator("script[src]").count()
                results["metrics"][device+"_page_errors"] = errors[:20]
                check(device+"_no_javascript_exceptions", len(errors) == 0)
                check(device+"_interactive_controls", results["metrics"][device+"_input_count"] + results["metrics"][device+"_button_count"] > 0)
                await page.screenshot(path=str(OUT / (device+".png")), full_page=False)
                # Testa uma entrada textual sem assumir seletores específicos da interface.
                text_inputs = page.locator('input[type="search"], input[type="text"], input:not([type])')
                if await text_inputs.count():
                    try:
                        target = text_inputs.first
                        await target.fill("こんにちは", timeout=4000)
                        results["metrics"][device+"_search_input_accepts_japanese"] = await target.input_value() == "こんにちは"
                    except Exception as e:
                        results["warnings"].append(device+"_search_input: "+str(e)[:200])
                else:
                    results["warnings"].append(device+": campo de pesquisa não identificado")
                await context.close()
            # SW não funciona em HTTP comum remoto; localhost é origem segura.
            context = await browser.new_context(service_workers="allow")
            page = await context.new_page()
            await page.goto("http://127.0.0.1:8765/index.html", wait_until="domcontentloaded", timeout=90000)
            await page.wait_for_timeout(3000)
            state = await page.evaluate("""async () => {
              if (!('serviceWorker' in navigator)) return 'unsupported';
              const registrations = await navigator.serviceWorker.getRegistrations();
              return registrations.map(r => ({scope:r.scope, active:!!r.active}));
            }""")
            results["metrics"]["service_worker_registrations"] = state
            await context.close()
            await browser.close()
    finally:
        server.terminate()
        (OUT / "report.json").write_text(json.dumps(results, ensure_ascii=False, indent=2))
        print(json.dumps(results, ensure_ascii=False, indent=2))
    if not all(results["checks"].values()):
        raise SystemExit(1)

asyncio.run(main())
