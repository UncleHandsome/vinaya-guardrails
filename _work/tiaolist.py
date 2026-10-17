# -*- coding: utf-8 -*-
"""條文清單：按卷尾標 (N)/(N竟) 切段，取每段最後一句「若比丘…」為該條戒文，依序出清单。
用法：python -X utf8 _work/tiaolist.py [檔序 如 11-21|22-30] [起條] [迄條]
"""
import glob
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = sys.argv[1] if len(sys.argv) > 1 else "11-21"
LO = int(sys.argv[2]) if len(sys.argv) > 2 else 1
HI = int(sys.argv[3]) if len(sys.argv) > 3 else 200
U = u"零一二三四五六七八九"


def cn2int(s):
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s)


f = [p for p in glob.glob(os.path.join(ROOT, "原文", "*.txt")) if TAG in os.path.basename(p)]
assert f, u"無原文檔 %s" % TAG
s = io.open(f[0], encoding="utf-8").read().replace("\r\n", "\n")
TAIL = re.compile(u"[(（]([〇零一二三四五六七八九十]{1,4})竟?[)）]")
RULE = re.compile(u"若比丘尼?[^。]{0,140}?波逸提。")

prev, n = 0, 0
for m in TAIL.finditer(s):
    try:
        k = cn2int(m.group(1))
    except ValueError:
        continue
    seg = s[prev:m.start()]
    rr = list(RULE.finditer(seg))
    if rr:
        n = max(n, k)
        if LO <= k <= HI:
            print(u"%3d｜%s" % (k, rr[-1].group(0).replace(u"\n", u"")[:80]))
    prev = m.end()
