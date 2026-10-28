# -*- coding: utf-8 -*-
"""第 69 輪・乙刀：全書案例自稱總數之歸位（134→138）・章級指針之覆核。
用法：python -X utf8 _work/hlfix69b.py [--go]
"""
import os as _hp_os, sys as _hp_sys
_hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__))))
import hulan_path as HP
import hashlib
import io
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
BAK = HP.bakpath("69b")
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
sha0 = hashlib.sha256(raw.encode("utf-8")).hexdigest()
N0 = len(L)
n = 0


def do(tag, snip, old, new, want=1, rng=None):
    global n
    lo, hi = rng or (0, len(L))
    hits = [i for i in range(lo, hi) if old in L[i]]
    cnt = sum(L[i].count(old) for i in hits)
    assert cnt == want, u"%s｜命中 %d（欲 %d）：%s" % (tag, cnt, want, old[:24])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  %s L%-5d ✓ %s → %s" % (tag, i + 1, old[:22], new[:22]))
    n += cnt


NCASE = sum(1 for l in L if re.match(u"^#### (?:★ )?案例", l))
assert NCASE == 138, u"實收案例 %d 則（欲 138）" % NCASE
print(u"實收案例 %d 則" % NCASE)

print(u"\n―― 壹・自稱總數――")
do(u"甲1", None, u"把全書一百三十四則案例", u"把全書一百三十八則案例")
# 其餘凡『一百三十四』之稱須逐一點名（第134條乃戒號，非案數，故只查帶『則／案』者）
left = [(i + 1, L[i][:80]) for i in range(len(L))
        if re.search(u"一百三十四(則|案)|134\s*(則|案)", L[i])]
print(u"  殘留自稱總數：%d 處 %s" % (len(left), left))

print(u"\n―― 貳・第十二章之指針覆核（章級者俱可通，故只印不動）――")
i12 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十二章"))
i13 = next(i for i, l in enumerate(L) if l.startswith(u"# 第十三章"))
for i, l in enumerate(L):
    if u"第十二章" in l and not (i12 <= i < i13) and i > i13:
        print(u"  L%-5d|%s" % (i + 1, l[:104]))

print(u"\n―― 叁・本段指針之落點實測（第十四章案例二／十七・第十五章案例七）――")
for ch, cs in [(u"第十四章", [u"案例二", u"案例十七"]), (u"第十五章", [u"案例七"])]:
    a = next(i for i, l in enumerate(L) if l.startswith(u"# " + ch))
    b = next(i for i in range(a + 1, len(L)) if re.match(u"^# 第[一二三四五六七八九十]+章", L[i]))
    for c in cs:
        hit = [i + 1 for i in range(a, b) if L[i].startswith(u"#### " + c)]
        print(u"  %s%s → %s" % (ch, c, hit or u"無此案"))

assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"\n共 %d 處改動｜行數 %d→%d" % (n, N0, len(L)))
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
