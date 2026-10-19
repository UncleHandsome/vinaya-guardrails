# -*- coding: utf-8 -*-
"""全冊掃圍欄之實字：每一字之字型・字級・advance/em 比。找出『ord<0x2E80 卻以全形（≈1.0em）出字』
   者——即 Consolas 缺字而後備到 Microsoft JhengHei 之框線／箭頭，為圖表散架之因。
   用法：python -X utf8 _work/_r55chars.py [pdf] [頁數上限]"""
import sys
from collections import defaultdict

import pymupdf as pm

PDF = sys.argv[1] if len(sys.argv) > 1 else '_print/book.pdf'
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 0
BOXISH = u'│├└┌┐─►◄▲▼●○◎◈◆■□★☆→←↑↓'
d = pm.open(PDF)
n = d.page_count if not CAP else min(CAP, d.page_count)
stat = defaultdict(lambda: [0, 0.0, 0.0])   # (char, font) -> [次, 最小比, 最大比]
for p in range(n):
    pg = d[p]
    for b in pg.get_text('rawdict')['blocks']:
        for ln in b.get('lines', []):
            txt = ''.join(c['c'] for sp in ln.get('spans', []) for c in sp['chars'])
            if not any(ch in txt for ch in BOXISH):
                continue                      # 只量圖表行
            for sp in ln.get('spans', []):
                sz = sp.get('size', 0)
                if not sz:
                    continue
                f = sp.get('font', '?')
                for c in sp.get('chars', []):
                    ch = c['c']
                    if ch.strip() == '':
                        continue
                    r = (c['bbox'][2] - c['bbox'][0]) / sz
                    s = stat[(ch, f)]
                    s[0] += 1
                    s[1] = min(s[1], r) if s[0] > 1 else r
                    s[2] = max(s[2], r) if s[0] > 1 else r
sus = []
for (ch, f), (c0, lo, hi) in stat.items():
    if ord(ch) < 0x2E80 and 'heng' in f.lower() and hi > 0.8:
        sus.append((ch, f, c0, lo, hi))
print(u'掃 %d 頁｜圖表行之『窄字而全形出字』 suspects：%d 種' % (n, len(sus)))
for ch, f, c0, lo, hi in sorted(sus, key=lambda x: -x[2])[:24]:
    print(u'   %s U+%04X｜%-26s ×%-6d｜advance/em %.2f–%.2f' % (ch, ord(ch), f[:26], c0, lo, hi))
half = [(ch, f, c) for (ch, f), (c, lo, hi) in stat.items() if ord(ch) < 0x2E80 and 'onsolas' in f]
print(u'（對照）Consolas 內之窄字：%d 種，其 advance/em 多在 0.55' % len(half))
d.close()
