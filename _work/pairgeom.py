# -*- coding: utf-8 -*-
"""印面幾何之全冊尺（第十波改）：不靠模型估版心，**自產物推出版心**。

舊病：本器原以 `版心右界約 555.3pt` 之推算為判準，又固定查第 #20 段圍欄（索引一動即錯位）；
      今實測兩冊之文字左界在 27.7pt（＝CSS 之外側 10mm），對稱之右界當為 595 − 27.7 = 567.3pt，
      而中文標點與末字可微量出界（實測最大 570.7pt，仍在紙內、非斷行失敗）——
      故判準改立：**右界逾 567.3 + 8pt 方為真出框**（8pt ≈ 2.8mm，逾此則字已近裁切線）。

用法：python -X utf8 _work/pairgeom.py [pdf…]   （缺＝兩冊螢幕版）
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import pymupdf as pm  # noqa: E402

TOL = 8.0
DEFAULT = ["_print/pair1.pdf", "_print/pair2.pdf"]
PDFS = sys.argv[1:] or DEFAULT

for name in PDFS:
    p = Path(ROOT) / name if not os.path.isabs(name) else Path(name)
    if not p.is_file():
        p = ROOT / "_print" / name
    d = pm.open(str(p))
    W = d[1].rect.width if d.page_count > 1 else d[0].rect.width
    lefts = []
    per = []
    for i in range(2, d.page_count):
        xs0, xs1 = [], []
        for b in d[i].get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for l in b["lines"]:
                for s in l["spans"]:
                    if s["bbox"][2] - s["bbox"][0] < 0.5:
                        continue
                    xs0.append(s["bbox"][0])
                    xs1.append(s["bbox"][2])
        if not xs0:
            continue
        lefts.append(min(xs0))
        per.append((i + 1, min(xs0), max(xs1)))
    d.close()
    m_out = min(lefts)                       # 外側邊距（自產物推出，非 CSS 之宣稱）
    bound = W - m_out
    over = [(pg, r) for pg, l, r in per if r > bound + TOL]
    near = [(pg, r) for pg, l, r in per if bound < r <= bound + TOL]
    tight = [(pg, l) for pg, l, r in per if l < m_out - 1.0]
    print("■ %s｜頁寬 %.1f・外側邊距 %.1f（實推）・版心右界 %.1f（+%d 容標點出界＝%.1f）"
          % (os.path.basename(p.name), W, m_out, bound, int(TOL), bound + TOL))
    print("   真出框之頁：%d%s" % (len(over), "" if not over else " ➔ " + str(over[:6])))
    print("   近界（標點微出，非病）：%d 頁・左界侵外側邊距之頁：%d" % (len(near), len(tight)))
    print("   全冊最大右界 %.1f・最小左界 %.1f" % (max(r for _, _, r in per), m_out))
