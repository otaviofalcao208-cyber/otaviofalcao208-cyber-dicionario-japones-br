#!/usr/bin/env python3
"""Gera arquivo offline com leituras e significados PT do KANJIDIC2 (EDRDG).
Dados licenciados sob CC BY-SA 4.0: https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
"""
import gzip
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

root = pathlib.Path(__file__).resolve().parent
joyo = list((root / "joyo-kanji.txt").read_text(encoding="utf-8").strip())
assert len(joyo) == len(set(joyo)) == 2136
url = "https://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
with urllib.request.urlopen(url, timeout=120) as response:
    xml = gzip.decompress(response.read())
tree = ET.fromstring(xml)
records = {}
without_pt = []
for entry in tree.findall("character"):
    ch = entry.findtext("literal")
    if ch not in joyo:
        continue
    rm = entry.find("reading_meaning/rmgroup")
    if rm is None:
        continue
    kun = [n.text for n in rm.findall("reading") if n.get("r_type") == "ja_kun" and n.text]
    on = [n.text for n in rm.findall("reading") if n.get("r_type") == "ja_on" and n.text]
    pt = [n.text for n in rm.findall("meaning") if n.get("m_lang") == "pt" and n.text]
    if not pt:
        without_pt.append(ch)
    if kun or on:
        records[ch] = [" / ".join((kun[:2] + on[:2])[:4]), ", ".join(pt[:3])]
missing = [ch for ch in joyo if ch not in records]
if missing:
    raise RuntimeError("Sem leituras para: " + "".join(missing))
if without_pt:
    raise RuntimeError("Sem significados em português: " + "".join(without_pt))
assert len(records) == 2136 and all(all(record) for record in records.values())
out = "/* KANJIDIC2 EDRDG, CC BY-SA 4.0 — https://www.edrdg.org/wiki/index.php/KANJIDIC_Project */\nwindow.KOTOBA_KANJI_DATA=" + json.dumps(records, ensure_ascii=False, separators=(",", ":")) + ";\n"
(root / "kanji-dados.js").write_text(out, encoding="utf-8")
print("Concluído: 2136 kanjis com leitura japonesa e significado português.")
