# -*- coding: utf-8 -*-
"""第 43 輪補刀：蒜案譏嫌語之逐字段含刪節號而跨了兩句（律中兩句之間另有「外自稱言…」），
   拆為兩段各自連写。用法：python -X utf8 _work/r10fix.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
GO = u"--go" in sys.argv
BOOK = HP.SRC
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
NV = _tk.norm(_tk.VINAYA)

OLD = u"居士當街譏嫌：「**比丘尼受取無厭足……正使檀越施與，猶應知足，況不見主而取盡！**」"
NEW = u"居士當街譏嫌：「**此比丘尼無有慚愧，受無厭足**」——一句之中又補一刀：「**正使檀越施與，猶應知足，況不見主而取盡**」"
for t in [u"此比丘尼無有慚愧，受無厭足", u"正使檀越施與，猶應知足，況不見主而取盡"]:
    assert _tk.norm(t) in NV, u"仍不連写：%s" % t
hits = [i for i, s in enumerate(L) if OLD in s]
assert len(hits) == 1, u"命中 %d" % len(hits)
L[hits[0]] = L[hits[0]].replace(OLD, NEW)
print(u"  ✓ L%-5d｜譏嫌語拆為兩段連写" % (hits[0] + 1))

# 全書覆納：以 hlchk 為法源，此處只斷「舊形已絕、新形俱連写」
assert not any(u"比丘尼受取無厭足" in s for s in L), u"舊形仍在"
for t in [u"此比丘尼無有慚愧，受無厭足", u"正使檀越施與，猶應知足，況不見主而取盡"]:
    assert _tk.norm(t) in NV
txt = u"\r\n".join(L)
assert txt.count(u"\r\n") == len(L) - 1
print(u"行數 %d｜%s" % (len(L), u"寫檔" if GO else u"覆核模式（未寫檔）"))
if GO:
    io.open(BOOK, u"w", encoding="utf-8", newline=u"").write(txt)
