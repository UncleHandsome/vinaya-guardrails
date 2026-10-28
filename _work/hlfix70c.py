# -*- coding: utf-8 -*-
"""第 70 輪・丙刀：散文之半形斜線歸全形（punctchk 之制：圍欄外『/』須 0）。
用法：python -X utf8 _work/hlfix70c.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = HP.bakpath("70c")
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()
OLD = u"Trade/Contract"
NEW = u"Trade／Contract"
hits = [i for i, l in enumerate(L) if OLD in l]
assert len(hits) == 1, u"錨見 %d 處（欲 1）：%s" % (len(hits), [x + 1 for x in hits])
for i in hits:
    print(u"  L%-5d ✓ %s" % (i + 1, L[i][max(0, L[i].index(OLD) - 24):L[i].index(OLD) + 30]))
    L[i] = L[i].replace(OLD, NEW)
assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
if not GO:
    print(u"（乾跑）")
    sys.exit(0)
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s" % (sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12]))
