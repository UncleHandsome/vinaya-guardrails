# -*- coding: utf-8 -*-
"""第 263 輪・探針：以『全書尺」之緊口徑（_simpdict 384＋語料自算豁免）覆量 ver39。

緣起：本冊 `_work/v39chk.py` 之簡形尺向用 `_simpmap.S`（233 枚），而全书尺 `simp_sweep.py`
      用 `_simpdict.MAP`（384 枚）——兩張字典未合一，實測已放過『让』『价』二枚（L5494・L7249）。
本針只量：依 384 之名單，ver39 之印面引號外（並另報『』之內）尚有幾枚簡形。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
from _simpdict import MAP as SIMP                                  # noqa: E402

NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
t = io.open(os.path.join(ROOT, NAME), encoding='utf-8-sig', newline='').read()

CORP = set()
for f in glob.glob(os.path.join(ROOT, u'原文', u'*.txt')):
    CORP |= set(io.open(f, encoding='utf-8', errors='ignore').read())
RISKY = {k for k in SIMP if k in CORP}

LINE0 = []
acc = 0
for l in t.split(u'\n'):
    LINE0.append(acc)
    acc += len(l) + 1


def lineno(i):
    lo, hi = 0, len(LINE0) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if LINE0[mid] <= i:
            lo = mid
        else:
            hi = mid - 1
    return lo + 1


PROTECT = [m.span() for m in re.finditer(u'「[^」\n]*」', t)]
PROTECT += [m.span() for m in re.finditer(u'『[^』\n]*』', t)]
PROTECT += [m.span() for m in re.finditer(u'\\[[^\\]\\n]{1,14}\\]', t)]
TERM = [m.span() for m in re.finditer(u'『[^』\n]*』', t)]
inq = lambda i, S=PROTECT: any(a <= i < b for a, b in S)
interm = lambda i: any(a <= i < b for a, b in TERM)

out, inner = {}, {}
for i, c in enumerate(t):
    if c not in SIMP or (c in RISKY and inq(i)):
        continue
    tgt = inner if interm(i) else out
    tgt.setdefault(c, []).append((lineno(i), c, SIMP[c],
                                  t[max(0, i - 12):i + 12].replace(u'\n', u'/')))
for tag, d in ((u'引號外（須改）', out), (u'『』之內（待判：編者語抑或照錄舊形）', inner)):
    n = sum(len(v) for v in d.values())
    print(u'——— %s：%d 種 %d 處' % (tag, len(d), n))
    for c, v in sorted(d.items()):
        for ln, a, b, ctx in v:
            print(u'   L%-6d %s→%s｜%s' % (ln, a, b, ctx))
import _simpmap as _SM                                            # noqa: E402
extra = set(SIMP) - set(_SM.S)
print(u'名單之比對：_simpdict %d 枚／_simpmap %d 枚／前者獨有 %d 枚（其中見於語料而自豁免者 %d 枚）' % (
    len(SIMP), len(set(_SM.S)), len(extra), len([c for c in extra if c in CORP])))
print(u'   前者獨有而未豁免：%s' % u''.join(sorted(c for c in extra if c not in CORP)))
