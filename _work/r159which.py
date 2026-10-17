# -*- coding: utf-8 -*-
"""r159which.py —— 出『真病之節』之名單並附上下文，供逐節親撰承接句（口徑同 readchk 第六目）。
用法：PYTHONPATH=. python _work/r159which.py [篇名關鍵字]
"""
import io, os, re, sys
import collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk as t

L = t.LINES
N = len(L)
BOT = set(t.bottom_lines())
FEN = [False] * N
_in = False
for i, l in enumerate(L):
    if l.strip().startswith(u'```'):
        _in = not _in
        FEN[i] = True
        continue
    FEN[i] = _in
PRINT = [i for i in range(N) if i not in BOT and not FEN[i]]
LISTY = re.compile(u'^([-*]\\s|\\d+[.)、]\\s|[（(][一二三四五六七八九十]+[）)])')
FLD = re.compile(u'^\\s*(?:[-*]|\\d+[.)、]|[一二三四五六七八九十]+[.)、])\\s*\\*\\*[^*]+\\*\\*[:：]')


def norm(x):
    return re.sub(u'^#+\\s*(?:\\d+[.、]\\s*)?', u'', x).strip()


def kind(i):
    s = L[i].strip()
    if s == u'':
        return u'空'
    if s.startswith(u'|'):
        return u'表'
    if s.startswith(u'#'):
        return u'題'
    if s.startswith(u'>'):
        return u'引'
    if LISTY.match(s):
        return u'列'
    if s in (u'---', u'***'):
        return u'線'
    return u'文'


HC = collections.Counter(norm(L[i]) for i in PRINT if L[i].startswith((u'#### ', u'##### ')))


def chap(i):
    for j in range(i, -1, -1):
        if L[j].startswith(u'# '):
            return L[j][2:18]
    return u'?'


KEY = sys.argv[1] if len(sys.argv) > 1 else None
rows = []
for i in PRINT:
    if not L[i].startswith((u'#### ', u'##### ')):
        continue
    j = i + 1
    while j < N and L[j].strip() == u'':
        j += 1
    if j >= N or j in BOT or FEN[j] or kind(j) not in (u'表', u'列'):
        continue
    k = j + 1
    while k < N and not L[k].startswith(u'#'):
        k += 1
    seg = [x for x in L[j:k] if x.strip()]
    if HC[norm(L[i])] >= 5 or (kind(j) == u'列' and seg and FLD.match(seg[0])
            and 2 * len([x for x in seg if FLD.match(x)]) >= len(seg)):
        continue
    rows.append((i + 1, kind(j), L[i].strip(), chap(i), j))
print(u'真病之節：%d' % len(rows))
for ln, kd, h, c, j in rows:
    if KEY and KEY not in c:
        continue
    print(u'【L%-6d｜%s｜%s】%s' % (ln, kd, c[:8], h[:62]))
    prev = [k for k in range(ln - 2, 0, -1) if L[k].strip() and not L[k].startswith(u'#')][:1]
    for k in prev:
        print(u'   上末：%s' % L[k].strip()[:70])
    print(u'   首行：%s' % L[j].strip()[:70])
