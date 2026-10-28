# -*- coding: utf-8 -*-
"""第 69 輪・丙刀：§三款式1 之條號歸位（尼波羅夷 1～4 之書中落點須由產生器認得）。
病：新稿只作『前四波羅夷（大僧同名而別宣）』，無『第1、2、3、4條』之號，
    產生器便無法為乙部前四行指派針，gapcensus 遂報『未展開 4／別宣 8』。
用法：python -X utf8 _work/hlfix69c.py [--go]
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
BAK = HP.bakpath("69c")
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()

OLD = u"#### 1. 根本底線：前四波羅夷（大僧同名而別宣）"
NEW = u"#### 1. 根本底線：前四波羅夷（第1、2、3、4條，大僧同名而尼端別宣）"
hits = [i for i, l in enumerate(L) if l == OLD]
assert len(hits) == 1, u"錨行見 %d 處（欲 1）" % len(hits)
L[hits[0]] = NEW
print(u"  L%-5d ✓ 補條號：%s" % (hits[0] + 1, NEW))
assert u"・" not in NEW and L[hits[0]].startswith(u"#### 1. "), u"形制破口"
assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
