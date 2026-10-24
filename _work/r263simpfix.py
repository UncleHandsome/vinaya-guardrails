# -*- coding: utf-8 -*-
"""第 263 輪・刀三：以『全書尺」之緊口徑（_simpdict 384）逮得之八枚簡形，逐枚歸正。

緣起：本冊舊尺用 `_simpmap.S`（233 枚），名單之外之『动・无・价・经・脱・过・项・让』八枚歷輪無報
      （`_work/r263simp.py` 之量）。正字一律取自 `_simpdict.MAP`，不憑記憶構碼位。
用法：python -X utf8 _work/r263simpfix.py [apply]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
from _simpdict import MAP as SIMP                                  # noqa: E402

NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
PATH = os.path.join(ROOT, NAME)
t = io.open(PATH, encoding='utf-8-sig', newline='').read()

# (行號, 含簡形之上下文錨) —— 錨須於全檔恰中一次
TARGETS = [(4549, u'小动作乃大病之前相'),
           (5494, u'『形式之退让不消滅實質之逼近』'),
           (6438, u'算清誰先踩了泥坑毫无意義'),
           (7249, u'靠的是守約，不是出价。'),
           (7406, u'四者任取其一经即得門徑'),
           (8693, u'物體脱離本處'),
           (8694, u'律中一切「过夜」「至三宿」'),
           (8904, u'歷來分项而治')]

plan = []
for ln, anchor in TARGETS:
    n = t.count(anchor)
    assert n == 1, (ln, anchor, n)
    simp = [c for c in anchor if c in SIMP]
    assert len(simp) >= 1, (ln, anchor)
    new = u''.join(SIMP[c] if c in SIMP else c for c in anchor)
    plan.append((ln, anchor, new, simp))

for ln, a, b, simp in plan:
    print(u'L%-6d %s ｜ %s ➔ %s' % (ln, u''.join(simp), a[:34], b[:34]))
if len(sys.argv) > 1:
    for _ln, a, b, _s in plan:
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    io.open(PATH, 'w', encoding='utf-8', newline='').write(t)
    chk = io.open(PATH, encoding='utf-8-sig', newline='').read()
    for _ln, a, b, _s in plan:
        assert chk.count(a) == 0, (a, chk.count(a))
        assert chk.count(b) == 1, (b, chk.count(b))
    print(u'已寫入八枚，回讀相符。')
else:
    print(u'乾跑，未寫入。')
