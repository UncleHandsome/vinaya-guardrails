# -*- coding: utf-8 -*-
"""目測取樣：把指定頁出圖（查驗收器「待考」之表是否真的完好）。
用法：python peekpage.py 55 s220（前綴 s 者出精簡本之頁）。"""
import os, sys
import pymupdf as fitz

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, '_print', 'ver38四分律_起心動念心智分析框架_第三十八版_列印版.pdf')
SLIM = os.path.join(ROOT, '_print', 'ver38四分律_起心動念心智分析框架_第三十八版_列印版_精簡本.pdf')
for a in sys.argv[1:]:
    # s220 之形 = 出精簡本之第 220 頁；裸數字則出完整版。两式頁界不同，故須分流指名。
    slim = a.startswith('s')
    p = int(a.lstrip('s'))
    doc = fitz.open(SLIM if slim else PDF)
    pix = doc[p - 1].get_pixmap(dpi=105)
    out = os.path.join(ROOT, '_work', 'peek_%sp%d.png' % ('s' if slim else '', p))
    pix.save(out)
    print(u'頁 %s%d → %s（繪圖 %d）' % ('精簡 ' if slim else '', p, os.path.basename(out), len(doc[p - 1].get_drawings())))
    doc.close()
