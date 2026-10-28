# -*- coding: utf-8 -*-
"""印面目視之代：兩冊＋合冊之空頁・留白之存數・綱要之落頁・字面 markdown 之殘。"""
import glob
import re

import pymupdf

P = {
    "F2": glob.glob("_print/如法推尋_*_螢幕版.pdf")[0],
    "F1": glob.glob("_print/起心動念_*_螢幕版.pdf")[0],
    "合冊": glob.glob("_print/雙子星合冊_*_螢幕版.pdf")[0],
}
BREATH = re.compile(r"【本章章末指針|【林下留白|章末指針與林下留白")
for tag, path in P.items():
    d = pymupdf.open(path)
    near = [(i, len(pg.get_text().strip())) for i, pg in enumerate(d, 1) if len(pg.get_text().strip()) < 45]
    br = [(i, BREATH.findall(pg.get_text())) for i, pg in enumerate(d, 1) if BREATH.search(pg.get_text())]
    print("■", tag, path.split("/")[-1][:40], "・", d.page_count, "頁")
    print("   近空之頁（篇題頁乃設計使然）:", near)
    print("   留白現形之頁:", [i for i, _ in br], "・計", sum(len(x) for _, x in br), "枚")
    for q in ("第一階・前置管轄與界之閥", "四署之名與職", "十六・消磁之檢"):
        hit = [i for i, pg in enumerate(d, 1) if q in pg.get_text()]
        print("   「%s」→ %s" % (q, hit[:4]))
    md = [(i, l) for i, pg in enumerate(d, 1) for l in pg.get_text().split("\n")
          if re.match(r"^\s*(#|\*\*|```|- \[ \])", l) or "_____" in l or "[ ]" in l]
    print("   字面 markdown・空格之殘:", md[:6], "・計", len(md))
