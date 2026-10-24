# -*- coding: utf-8 -*-
"""通用・掃腳本內之簡形（附上下文）。用法：python -X utf8 _work/r282sweep.py <腳本名...>"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _simpdict  # noqa: E402
import _simpmap  # noqa: E402

SIMP = set(_simpdict.MAP.keys()) | set(getattr(_simpmap, 'MAP', {}).keys())
tot = 0
for fn in sys.argv[1:]:
    p = fn if os.path.isabs(fn) else os.path.join(ROOT, u'_work', fn)
    S = io.open(p, encoding=u'utf-8').read()
    hits = sorted({c for c in S if c in SIMP})
    print(u'%s：簡形 %d 種【%s】' % (os.path.basename(p), len(hits), u''.join(hits)))
    tot += len(hits)
    for c in hits:
        n = 0
        pos = -1
        while n < 3:
            pos = S.find(c, pos + 1)
            if pos < 0:
                break
            n += 1
            print(u'  「%s」U+%04X 第%d見 …%s…' % (
                c, ord(c), n, S[max(0, pos - 26):pos + 26].replace(u'\n', u'\\n')))
print(u'合計：%d 種' % tot)
sys.exit(1 if tot else 0)
