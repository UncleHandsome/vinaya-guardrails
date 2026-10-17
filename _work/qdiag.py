# -*- coding: utf-8 -*-
"""定位無據引文之断點：取最長可中之前綴，並印出斷點前後之草稿形與語料形。
用法：python _work/qdiag.py <檔案> <片段序號或子串>
"""
import io
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import _tk  # noqa: E402

t = io.open(sys.argv[1], encoding="utf-8").read()
key = sys.argv[2]
qs = [m.group(1) for m in re.finditer(u"「(.+?)」", t, re.S)]
cand = [q for q in qs if key in q]
for q in cand[:2]:
    n = _tk.norm(q)
    lo, hi = 0, len(n)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if n[:mid] in _tk.VINAYA:
            lo = mid
        else:
            hi = mid - 1
    print(u"引文：%s" % q.replace("\n", "/"))
    print(u"最長可中之前綴（%d/%d）：%s" % (lo, len(n), n[:lo]))
    print(u"斷點之後：%s" % n[lo:lo + 26])
    print(u"語料同段：%s" % _tk.VINAYA[_tk.VINAYA.find(n[:lo]):_tk.VINAYA.find(n[:lo]) + lo + 40])
    print(u"---")
