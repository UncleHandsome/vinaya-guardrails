# -*- coding: utf-8 -*-
"""波逸提條次之本地推算：戒文之後最近之『N竟』尾標即其次第（本律自標之數，非外來表）。

用法：python -X utf8 _work/pairtiaoci.py 戒文首句 [戒文首句…]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk  # noqa: E402

V = _tk.VINAYA
P, MAP = [], []
for i, c in enumerate(V):
    if "\u4e00" <= c <= "\u9fff":
        MAP.append(i)
        P.append(_tk.FOLD.get(c, c))
P = "".join(P)
TAIL = re.compile(r"[〇一二三四五六七八九十百千]{1,6}竟")

for key in (sys.argv[1:] or ["若比丘知如是語人未作法如是邪見而不捨"]):
    p = "".join(_tk.FOLD.get(c, c) for c in re.sub(r"[^\u4e00-\u9fff]", "", key))
    j = P.find(p)
    print("「%s」%s" % (key, "命中" if j >= 0 else "★本地無"))
    if j < 0:
        continue
    o = MAP[j]
    m = TAIL.search(V[o:o + 2600])
    print("   其後最近之尾標：%s" % (m.group(0) if m else "未見"))
    ctx = re.sub(r"\s+", "", V[o:o + 240])
    print("   戒文窗：「%s」" % ctx[:200])
    # 往前找條目起首『若比丘…波逸提』之上一尾標，以定其序
    prev = None
    for mm in TAIL.finditer(V[max(0, o - 3000):o]):
        prev = mm.group(0)
    print("   前一尾標：%s｜故本條依本律尾標為【%s】" % (prev, m.group(0) if m else "?"))
