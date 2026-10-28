# -*- coding: utf-8 -*-
"""列全書圍欄圖：段序・源檔行・行數・寬格・所屬章節・最近之標題行（圖前導言）。"""
import os
import io
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hulan_path as HP

cw_units = lambda s: sum(2 if ord(c) > 0x2E80 else 1 for c in s)   # 與 build_hulan.cw_units 同式

L = io.open(HP.SRC, encoding="utf-8", newline=u"").read().split(u"\r\n")
F = u"```"
h = s = ""
op = None
n = 0
out = []
for i, l in enumerate(L):
    if l.startswith(u"# "):
        h, s = l[2:30], u""
    elif l.startswith(u"## "):
        s = l[3:34]
    elif l.startswith(u"### "):
        s = l[4:36]
    elif l.startswith(u"#### "):
        s = l[5:36]
    if l.startswith(F):
        if op is None:
            op = (i, h, s)
        else:
            n += 1
            body = L[op[0] + 1:i]
            w = max(cw_units(x) for x in body) if body else 0
            lead = u""
            for k in range(op[0] - 1, max(0, op[0] - 6), -1):
                if L[k].strip():
                    lead = re.sub(u"[*\\s]", u"", L[k])[:22]
                    break
            out.append((n, op[0] + 1, i + 1, len(body), w, op[1], op[2], lead))
            op = None
print(u"%-4s %-12s %4s %4s  %-24s %s" % (u"段", u"源檔行", u"行", u"格", u"所在", u"圖前導言"))
for n, a, b, ln, w, hh, ss, lead in out:
    print(u"%-4d L%-5d–%-5d %4d %4d  %-24s %s" % (n, a, b, ln, w, (ss or hh)[:24], lead))
print(u"共 %d 段" % n)
