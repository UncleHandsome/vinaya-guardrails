# -*- coding: utf-8 -*-
"""精簡本改標之實測：PDF 與中介 md 兩側俱數『定本附錄X』與未改標之裸『附錄X』。"""
import io, os, re, sys
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PR = os.path.join(ROOT, "_print")
TAGGED = "定本附錄\\s*([CDEFGHIJKLM])"
BARE = "(?<!定本)附錄\\s*([CDEFGHIJKLM])"

cases = [
    ("精簡本 PDF", os.path.join(PR, "ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf")),
    ("精簡本中介 md", os.path.join(PR, "ver38_列印版_精簡本.md")),
    ("完整版中介 md", os.path.join(PR, "ver38_列印版.md")),
]
out = []
for name, path in cases:
    if not os.path.exists(path):
        out.append("缺檔 " + path)
        continue
    if path.endswith(".pdf"):
        d = pymupdf.open(path)
        s = "".join(p.get_text() for p in d)
        d.close()
        s = re.sub(r"\s+", "", s)
    else:
        s = io.open(path, encoding="utf-8").read()
    t = re.findall(TAGGED, s)
    b = re.findall(BARE, s)
    out.append("%-14s 定本附錄X %2d（%s）｜裸附錄X %2d（%s）"
               % (name, len(t), "".join(sorted(set(t))), len(b), "".join(sorted(set(b))) or "無"))
io.open(os.path.join(ROOT, "_work", "appxtag89.txt"), "w", encoding="utf-8").write(
    "\n".join(out) + "\n")
sys.stdout.write("\n".join(out) + "\n")
