#!/usr/bin/env python3
"""Gera modelos de escrita locais para os 2136 jōyō kanji a partir do KanjiVG.
Fonte: https://github.com/KanjiVG/kanjivg (CC BY-SA 3.0).
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

root=pathlib.Path(__file__).resolve().parent
kanjivg=pathlib.Path(sys.argv[1])
joyo=list((root/"joyo-kanji.txt").read_text(encoding="utf-8").strip())
assert len(joyo)==2136 and len(set(joyo))==2136, "Lista jōyō inválida"
existing=(root/"tracos.js").read_text(encoding="utf-8")
models=json.loads(existing.split("window.KOTOBA_STROKES=",1)[1].rstrip().removesuffix(";"))
missing=[]
for char in joyo:
    path=kanjivg/"kanji"/f"{ord(char):05x}.svg"
    if not path.exists():
        missing.append(char)
        continue
    tree=ET.parse(path)
    paths=[element.attrib["d"] for element in tree.iter() if element.tag.endswith("}path") and "d" in element.attrib]
    if not paths:
        missing.append(char)
    else:
        models[char]=paths
if missing:
    raise SystemExit("KanjiVG sem modelos para: "+"".join(missing))
assert all(char in models for char in joyo)
out="/* KanjiVG CC BY-SA 3.0: https://github.com/KanjiVG/kanjivg */\nwindow.KOTOBA_STROKES="+json.dumps(models,ensure_ascii=False,separators=(",",":"))+";\n"
(root/"tracos.js").write_text(out,encoding="utf-8")
print(f"Modelos: {len(models)} caracteres; 2136 jōyō kanji.")
