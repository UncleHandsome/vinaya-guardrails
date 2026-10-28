# -*- coding: utf-8 -*-
"""第 70 輪・乙刀：全書自稱總數（138→137）・跨章指針歸位・新第十三章之指針覆核。
教（本輪自犯）：入冊刀 丁5 把『尼單提第156條著襯體衣戒』系於第十四章案例二——該條在第125～178
    段，實屬第十五章案例二。跨章指針之章次不可凭印象，須以條號落於何章之『範圍宣稱』定之。
用法：python -X utf8 _work/hlfix70b.py [--go]
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
BAK = HP.bakpath("70b")
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n") == raw.count(u"\r\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0, sha0 = len(L), hashlib.sha256(raw.encode("utf-8")).hexdigest()
n = 0


def do(tag, old, new, want=1):
    global n
    hits = [i for i, l in enumerate(L) if old in l]
    cnt = sum(L[i].count(old) for i in hits)
    assert cnt == want, u"%s｜命中 %d（欲 %d）：%s" % (tag, cnt, want, old[:30])
    for i in hits:
        L[i] = L[i].replace(old, new)
        print(u"  %-5s L%-5d ✓ %s ➔ %s" % (tag, i + 1, old[:30], new[:30]))
    n += cnt


NCASE = sum(1 for l in L if re.match(u"^#### (?:★ )?案例", l))
assert NCASE == 137, u"實收案例 %d 則（欲 137）" % NCASE
print(u"實收案例 %d 則｜全書 %d 行" % (NCASE, N0))

print(u"\n―― 壹・自稱總數 ――")
do(u"甲1", u"把全書一百三十八則案例", u"把全書一百三十七則案例")
left = [(i + 1, l[:70]) for i, l in enumerate(L)
        if re.search(u"一百三十(?:(?!七則)|[一二三四五六八九十])則|全書[一二三四五六七八九十百]+則案例", l)
        and u"一百三十七則案例" not in l]
print(u"  殘留自稱總數（應唯實數 137）：%s" % (left or u"無"))

print(u"\n―― 貳・跨章指針歸位 ――")
# 本輪入冊刀之錯系：第156條在后半部（第125～178），屬第十五章案例二而非第十四章
# 只削『章次』二字，不碰戒名（戒名之『襯體』二字形難打，重打即錯——本刀首版即誤植為『諔』）
do(u"乙1", u"之前哨，見第十四章案例二", u"之前哨，見第十五章案例二")

print(u"\n―― 叁・全書指針之落點覆核（點名實題，不符即擲）――")
U = u"零一二三四五六七八九十"


def cn2int(s):
    if len(s) == 1:
        return U.index(s)
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    if len(s) == 2:                                    # 「十九」之類：十前之數乘十再加後數
        return U.index(s[0]) * 10 + U.index(s[1])
    return None


CH = re.compile(u"^# 第([一二三四五六七八九十]+)章")
heads = {}
for i, l in enumerate(L):
    m = CH.match(l)
    if m:
        c = cn2int(m.group(1))
        assert c, u"L%d 章次『%s』歸數失敗" % (i + 1, m.group(1))
        heads[c] = i


def title_of(chap, case):
    a = heads[chap]
    b = next((heads[k] for k in sorted(heads) if k > chap), len(L))
    for i in range(a, b):
        m = re.match(u"^#### (?:★ )?案例([一二三四五六七八九十]+)：(.*)$", L[i])
        if m and cn2int(m.group(1)) == case:
            return L[i][5:][:64]
    return None


bad = []
for i, l in enumerate(L):
    if l.startswith(u"# 附錄"):
        break
    for m in re.finditer(u"第([一二三四五六七八九十]+)章案例([一二三四五六七八九十]+)", l):
        c, k = cn2int(m.group(1)), cn2int(m.group(2))
        if c not in heads:
            bad.append((i + 1, m.group(0), u"無此章"))
            continue
        t = title_of(c, k)
        if t is None:
            bad.append((i + 1, m.group(0), u"該章無此案"))
print(u"  指針失指：%d 處" % len(bad))
for i, w, why in bad:
    print(u"    × L%-5d %s｜%s" % (i, w, why))
    print(u"        上下文：%s" % L[i - 1][:100] if i > 0 else u"")

assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n") == len(L) - 1, u"CRLF 變形"
print(u"\n共 %d 處改動｜失指 %d 處" % (n, len(bad)))
if not GO:
    print(u"（乾跑：加 --go 始寫檔）")
    sys.exit(0)
assert not bad, u"尚有失指，不敢寫檔"
if not os.path.exists(BAK):
    shutil.copy2(BOOK, BAK)
with open(BOOK, "wb") as fh:
    fh.write(txt.encode("utf-8"))
chk = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert chk == txt, u"回讀不符"
print(u"已寫檔｜sha %s→%s｜備份 %s" % (
    sha0[:12], hashlib.sha256(chk.encode("utf-8")).hexdigest()[:12], os.path.basename(BAK)))
