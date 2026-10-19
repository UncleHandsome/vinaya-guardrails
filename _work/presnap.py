# -*- coding: utf-8 -*-
"""取印面之圍欄圖頁，轉 PNG 供目視（框線是否對齊、是否斷頁）。
   用法：python -X utf8 _work/_r55shot.py [pdf] [关键字…]"""
import os
import sys

import pymupdf as pm

PDF = sys.argv[1] if len(sys.argv) > 1 else '_print/book.pdf'
KEYS = sys.argv[2:] or [u'【全書全景結構圖】', u'【事件現前', u'【第一階：根基門】',
                        u'【針對犯而不見罪者】', u'【定罪判決生效', u'【僧團司法程序總圖】']
d = pm.open(PDF)
BOX = u'│├└─┌┐┘▲▼◎◈'
hits = []
for i in range(d.page_count):
    t = d[i].get_text()
    n = sum(t.count(c) for c in BOX)
    if n > 40:
        hits.append((i, n))
print(u'框線字最多之頁：%s（全冊 %d 頁）' % (hits[:8], d.page_count))
seen = set()
for k in KEYS:
    pg = next((i for i in range(d.page_count) if k.replace(u' ', u'') in
               ''.join(d[i].get_text().split())), None)
    if pg is None or pg in seen:
        print(u'  未尋得：%s' % k[:20])
        continue
    seen.add(pg)
    out = '_work/_r55p%d.png' % (pg + 1)
    pix = d[pg].get_pixmap(dpi=150)
    pix.save(out)
    print(u'  取頁 %-4d｜%s｜%s' % (pg + 1, k[:22], out))
d.close()
