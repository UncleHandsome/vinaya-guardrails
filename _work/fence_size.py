# -*- coding: utf-8 -*-
"""圍欄圖印面體檢（口徑與 build_hulan.pre_overflows 同源）：
逐段量所在頁、格寬、現字級、可用寬，並回算「欲印達 9.4／10.0／10.8pt 所容之最大格寬」。
用法：python -X utf8 _work/fence_size.py [PDF]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_print"))
import pymupdf  # noqa: E402
from build_hulan import cw_units  # noqa: E402（只借格寬模型，勿跑 main）

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_print", "佛陀的護欄_四分律戒律之行為心理學解析_影印版.pdf")
BOOK = HP.SRC

lines = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
blocks, cur = [], None
for s in lines:
    if s.strip().startswith("```"):
        if cur is None:
            cur = []
        else:
            blocks.append(cur)
            cur = None
    elif cur is not None:
        cur.append(s)

d = pymupdf.open(PDF)
nn = lambda s: "".join(s.split())  # noqa: E731
pages = [nn(d[i].get_text()) for i in range(d.page_count)]
print("冊：%s｜%d 頁｜圍欄 %d 段" % (os.path.basename(PDF)[:20], d.page_count, len(blocks)))
print("%-3s %-5s %-4s %-7s %-7s %-8s %-8s %-8s %s"
      % ("序", "頁", "格寬", "現級", "可用pt", "≤9.4級", "≤10.0級", "≤10.8級", "須否重排"))
for k, b in enumerate(blocks, 1):
    head, tail = nn(b[0])[:12], nn(b[-1])[:12]
    at = next((i for i, t in enumerate(pages) if head in t and tail in t), None)
    if at is None:
        print("%-3d %-5s 未定位（跨頁或佚）" % (k, "?"))
        continue
    rows = []
    for bl in d[at].get_text("rawdict")["blocks"]:
        for ln in bl.get("lines", []):
            txt = "".join(c["c"] for sp in ln.get("spans", []) for c in sp["chars"])
            if not txt.strip():
                continue
            sz = min(sp.get("size", 99.0) for sp in ln.get("spans", []))
            rows.append((ln["bbox"][1], ln["bbox"][0], sz, nn(txt)))
    ys = [r[0] for r in rows if r[3].startswith(head)]
    ye = [r[0] for r in rows if r[3].startswith(tail)]
    seg = [r for r in rows if ys[0] - 1 <= r[0] <= max(ye) + 2]
    x0 = min(r[1] for r in seg)
    size = min(r[2] for r in seg)
    box = [g["rect"] for g in d[at].get_drawings()
           if g.get("fill") and seg[0][0] - 2 <= g["rect"].y0 <= max(ye) + 2
           and g["rect"].x0 <= x0 + 1 and g["rect"].x1 > x0 + 100]
    right = min((r.x1 for r in box), default=d[at].rect.width - 51.0)
    avail = right - 0.55 * size - 1.2 - x0
    W = max(cw_units(x) for x in b)
    cap = lambda s: int(avail / (0.55 * s))  # noqa: E731
    verdict = "重排至 ≤%d" % cap(9.4) if W > cap(9.4) else "可放大至 ≤%d" % cap(10.8)
    print("%-3d %-5d %-4d %-7.2f %-8.1f %-8d %-8d %-8d %s"
          % (k, at + 1, W, size, avail, cap(9.4), cap(10.0), cap(10.8), verdict))
d.close()
