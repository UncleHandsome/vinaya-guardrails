# -*- coding: utf-8 -*-
"""把源檔每一段圍欄圖，於 PDF 中找到所在頁並出圖，供目視核對框線對齊。
用法：python _work/hl_render.py <PDF> <出圖目錄> [序號…]
判準：以該段圍欄「首行＋末行」去空白後同見於一頁者為所在頁（圍欄本不許跨頁，故必存在）。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
PDF, OUT = sys.argv[1], sys.argv[2]
ONLY = [int(x) for x in sys.argv[3:]]
os.makedirs(OUT, exist_ok=True)


def n(s):
    return "".join(s.split())


L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
blocks, inf, buf = [], False, []
for l in L:
    if l.startswith("```"):
        if not inf:
            inf, buf = True, []
        else:
            inf = False
            if buf:
                blocks.append((buf[0], buf[-1]))
        continue
    if inf and l.strip():
        buf.append(l)
doc = pymupdf.open(PDF)
pages = [n(doc[i].get_text()) for i in range(doc.page_count)]
print(u"源檔圍欄 %d 段" % len(blocks))
for k, (a, b) in enumerate(blocks, 1):
    if ONLY and k not in ONLY:
        continue
    ka, kb = n(a)[:12], n(b)[:12]
    at = next((i for i, t in enumerate(pages) if ka in t and kb in t), None)
    if at is None:
        print(u"  %2d 查無同頁（首=%s｜末=%s）" % (k, ka[:8], kb[:8]))
        continue
    p = os.path.join(OUT, "f%02d_p%03d.png" % (k, at + 1))
    doc[at].get_pixmap(dpi=150).save(p)
    print(u"  %2d → p%-4d %s" % (k, at + 1, os.path.basename(p)))
