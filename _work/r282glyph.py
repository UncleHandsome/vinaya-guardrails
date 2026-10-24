# -*- coding: utf-8 -*-
"""282・驗字：把 r282matrix.FIX 之全部字串取出，掃簡形＋印難字碼位＋印全文供目視。"""
import importlib.util
import io
import os
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))

spec = importlib.util.spec_from_file_location(
    u'r282m', os.path.join(ROOT, u'_work', u'r282matrix.py'))
mod = importlib.util.module_from_spec(spec)
out = io.StringIO()
_real = sys.stdout
sys.stdout = out
try:
    spec.loader.exec_module(mod)
except SystemExit as e:
    print(u'（被驗模組自結 SystemExit %s）' % (e.code,))
finally:
    sys.stdout = _real
    sys.stdout.flush()
print(u'（乾跑輸出）\n' + out.getvalue())

import _simpdict  # noqa: E402
import _simpmap  # noqa: E402

SIMP = set(_simpdict.MAP.keys()) | set(_simpmap.MAP.keys()) if hasattr(_simpmap, 'MAP') else set(_simpdict.MAP.keys())
print(u'簡形字典：%d 鍵（另有 _simpmap %s）' % (
    len(_simpdict.MAP), sorted(x for x in dir(_simpmap) if not x.startswith('_'))))

NEED = u'波羅夷偷蘭遮僧殘突吉羅摩那埵別住羯磨比丘沙彌犯緣開緣爭點處斷戒體增上慢'
seen = {}
bad = []
for n in sorted(mod.FIX):
    for k, txt in enumerate(mod.FIX[n]):
        for ch in txt:
            if u'\u4e00' <= ch <= u'\u9fff':
                seen[ch] = seen.get(ch, 0) + 1
                if ch in SIMP:
                    bad.append((n, k, ch))
print(u'字種計數：%d 字・總 occurrences %d' % (len(seen), sum(seen.values())))
print(u'簡形命中：%d 枚' % len(bad))
for x in bad:
    print(u'  案%s 欄%d 「%s」U+%04X' % (x[0], x[1], x[2], ord(x[2])))
    ctx = mod.FIX[x[0]][x[1]]
    for j, c in enumerate(ctx):
        if c == x[2]:
            print(u'      …%s…' % ctx[max(0, j - 12):j + 12])
for ch in NEED:
    if ch not in seen:
        print(u'  \u672a\u898b\u96e3\u5b57\uff1a%s' % ch)
print(u'\u2500\u2500 \u5168\u6587 \u2500\u2500')
for n in sorted(mod.FIX):
    print(u'[%d] \u5f81\uff1a%s' % (n, mod.FIX[n][0]))
    print(u'[%d] \u65b7\uff1a%s' % (n, mod.FIX[n][1]))
