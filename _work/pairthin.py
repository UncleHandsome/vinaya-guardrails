# -*- coding: utf-8 -*-
"""細查：字面 `**` 之落點（散文或圍欄圖內）與 9pt 以下之頁分布。

用法：python -X utf8 _work/pairthin.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_print"))
sys.path.insert(0, str(ROOT))
sys.argv = ["build38", "full", "screen"]
import build_hulan as bh        # noqa: E402
import pymupdf as pm            # noqa: E402

PAIR = [("1", "起心動念", "pair1_screen.pdf", "pair_1_screen.md"),
        ("2", "如法推尋", "pair2_screen.pdf", "pair_2_screen.md")]

for key, name, pdfn, mdn in PAIR:
    pdf = ROOT / "_print" / pdfn
    md = ROOT / "_print" / mdn
    lines = io.open(md, encoding="utf-8").read().split("\n")
    fence_of, inf = [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            inf = not inf
            continue
        fence_of.append(inf)
    stars_src = [(i + 1, l.strip()[:60], fence_of[i]) for i, l in enumerate(lines)
                 if "**" in l and i < len(fence_of)]
    d = pm.open(str(pdf))
    pages = [(i + 1, [ln.strip() for ln in d[i].get_text().split("\n") if "**" in ln])
             for i in range(d.page_count)]
    pages = [(p, xs) for p, xs in pages if xs]
    thin = {}
    for i in range(d.page_count):
        for b in d[i].get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    if sp["text"].strip() and sp["size"] < 9:
                        thin.setdefault(i + 1, [0, 99])
                        thin[i + 1][0] += 1
                        thin[i + 1][1] = min(thin[i + 1][1], round(sp["size"], 2))
    d.close()
    print("=" * 72)
    print("■ %s｜中介 md 含 `**` 之原行 %d 行（其中圍欄內 %d・散文 %d）"
          % (name, len(stars_src), sum(1 for _i, _s, f in stars_src if f),
             sum(1 for _i, _s, f in stars_src if not f)))
    print("  冊上見字面 ** 之頁：%d 頁" % len(pages))
    for p, xs in pages[:8]:
        print("     p%-4d %s" % (p, " ‖ ".join(x[:44] for x in xs[:2])))
    print("  9pt 以下之頁分布：%s"
          % "・".join("p%d(%d span・最細 %spt)" % (k, v[0], v[1]) for k, v in sorted(thin.items())))
