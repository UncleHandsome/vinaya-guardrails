# -*- coding: utf-8 -*-
"""第 48 輪末修：第十六章按語之序——律文在前、史家之判在後，去其自我重複。"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "_work")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)
PAIRS = [
    (u"據後世史家所記，佛滅百年之後毘舍離一帶的比丘重啟的正是這一族問題（所謂十事），"
     u"長老堅不退轉，教團由此分為上座、大眾兩系——即佛教史通說之『根本分裂』。"
     u"此事不必假外求——本律自己就記著：",
     u"佛滅百年之後，毘舍離一帶的比丘重啟的正是這一族問題——此事不必假外求，本律自己就記著："),
    (u"至於上座、大眾二分之名與因果之判，出後世史家與部派之書，非此文逐字，本書不作律據。",
     u"而『長老不退轉，教團遂分上座、大眾兩系』——即佛教史通說之『根本分裂』——這一路判語出自後世史家與部派之書，"
     u"非此段之文，本書不作律據。"),
]
for old, new in PAIRS:
    ns = [i for i, t in enumerate(L) if old in t]
    assert len(ns) == 1 and L[ns[0]].count(old) == 1, (u"命中", old[:16], len(ns))
    L[ns[0]] = L[ns[0]].replace(old, new)
    print(u"改 @L%d（%d → %d 字）" % (ns[0] + 1, len(old), len(new)))

from _simpdict import MAP as SIMP  # noqa: E402
bad = sorted({c for _, n in PAIRS for c in n if c in SIMP})
print(u"新文簡形：%s" % ([(c, SIMP[c]) for c in bad] or 0))
assert len(L) == n0
out = NL.join(L)
print(u"行數 %d ｜ CR %d" % (len(L), out.count(chr(13))))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑）")
