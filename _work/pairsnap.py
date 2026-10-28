# -*- coding: utf-8 -*-
"""印面截圖（目視之用）：python -X utf8 _work/pairsnap.py <pdf 檔名於 _print/> 頁碼…

圖落 _work/（gitignore 內・隨手可重生成）。
"""
import sys
from pathlib import Path

import pymupdf as pm

ROOT = Path(__file__).resolve().parents[1]
pdf = ROOT / "_print" / sys.argv[1]
pages = [int(a) for a in sys.argv[2:]] or [1]
d = pm.open(str(pdf))
for p in pages:
    if not 1 <= p <= d.page_count:
        print("頁碼越界：%d（冊共 %d 頁）" % (p, d.page_count))
        continue
    pix = d[p - 1].get_pixmap(matrix=pm.Matrix(2, 2), alpha=False)
    out = ROOT / "_work" / ("%s_p%d.png" % (pdf.stem[:18], p))
    pix.save(str(out))
    print("✓", out.name, "%dx%d px" % (pix.width, pix.height))
d.close()
