#!/usr/bin/env python3
"""Gera dados locais dos 2136 Jōyō Kanji: KANJIDIC2 (EDRDG) e tradução EN→PT.
Fonte: https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
"""
import gzip, json, pathlib, urllib.request, xml.etree.ElementTree as ET
root=pathlib.Path(__file__).resolve().parent
joyo=list((root/"joyo-kanji.txt").read_text(encoding="utf-8").strip())
assert len(joyo)==2136 and len(set(joyo))==2136
url="https://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
with urllib.request.urlopen(url,timeout=120) as response:
    xml=gzip.decompress(response.read())
tree=ET.fromstring(xml)
records={}
for entry in tree.findall("character"):
    ch=entry.findtext("literal")
    if ch not in joyo: continue
    rm=entry.find("reading_meaning/rmgroup")
    if rm is None: continue
    on=[n.text for n in rm.findall("reading") if n.get("r_type")=="ja_on" and n.text]
    kun=[n.text for n in rm.findall("reading") if n.get("r_type")=="ja_kun" and n.text]
    meanings=[n.text for n in rm.findall("meaning") if n.get("m_lang") is None and n.text]
    if on or kun:
        readings=(kun[:2]+on[:2])[:4]
        records[ch]=[" / ".join(readings),", ".join(meanings[:3])]
missing=[ch for ch in joyo if ch not in records]
if missing: raise RuntimeError("KANJIDIC2 sem entradas: "+"".join(missing))
# Modelo de tradução instalado na geração; o aplicativo não faz chamadas online.
import argostranslate.package, argostranslate.translate
argostranslate.package.update_package_index()
models=[p for p in argostranslate.package.get_available_packages() if p.from_code=="en" and p.to_code=="pt"]
if not models: raise RuntimeError("Modelo de tradução inglês-português indisponível")
argostranslate.package.install_from_path(models[0].download())
translator=argostranslate.translate.get_translation_from_codes("en","pt")
cache={}
for ch,(read,english) in records.items():
    if english not in cache:
        translated=translator.translate(english).strip()
        cache[english]=translated if translated else english
    records[ch]=[read,cache[english]]
assert len(records)==2136
out="/* Dados offline: leituras KANJIDIC2 (EDRDG), significados traduzidos para PT. */\nwindow.KOTOBA_KANJI_DATA="+json.dumps(records,ensure_ascii=False,separators=(",",":"))+";\n"
(root/"kanji-dados.js").write_text(out,encoding="utf-8")
print(f"Gerados {len(records)} kanjis com leitura e significado em português.")
