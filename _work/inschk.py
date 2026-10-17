# -*- coding: utf-8 -*-
"""插入覆核：草稿每一塊（含標題至隔線）須以完全相同之行序出現在書中，且該章案例序號連貫。
口徑：空行不入比對、行尾半形空白不計（markdown 斷行用）；兩側先以 `_simpdict` 歸形再比，
     免「插入後補字典並全書掃形」把已在書中的塊報成缺席（第廿九輪之器病）。
用法：python -X utf8 _work/inschk.py <草稿檔>
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _simpdict import MAP as SIMP  # noqa: E402  歸形之單一法源

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
d = io.open(sys.argv[1], encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")

blocks, cur = [], None
for ln in d:
    if ln.startswith("#CH "):
        if cur is not None:
            blocks.append((ch, cur))
        ch, cur = int(ln[4:].strip()), []
    elif cur is not None:
        cur.append(ln.rstrip())
if cur is not None:
    blocks.append((ch, cur))
blocks = [(c, [x.rstrip() for x in b if x.strip()]) for c, b in blocks]

CHH = re.compile(u"^# 第(.+?)章")
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


st = [(cn2int(m.group(1)), i) for i, l in enumerate(L) for m in [CHH.match(l)] if m]
idx = {n: (st[k][1], st[k + 1][1] if k + 1 < len(st) else len(L)) for k, n in enumerate([x[0] for x in st])}

bad = 0


def canon(s):
    """兩側先以簡形字典歸一再比：插入之後若又補字典並全書掃形（simp_sweep fix），
       草稿仍存舊形，逐字比對便會把已在書中的塊報成『缺席』——此屬器病，非書病。"""
    return u"".join(SIMP.get(c, c) for c in s)


for c, b in blocks:
    a, z = idx[c]
    zpr = [(a + i, x.rstrip()) for i, x in enumerate(L[a:z]) if x.strip()]
    zone = [canon(x) for _, x in zpr]
    b = [canon(x) for x in b]
    joined = u"\n".join(b)
    hit = [i for i in range(len(zone) - len(b) + 1) if zone[i:i + len(b)] == b]
    head = b[0][:34]
    if not hit:
        bad += 1
        print(u"  缺席｜第%s章「%s」（%d 行）" % (c, head, len(b)))
        continue
    num = re.match(u"#### 案例([〇零一二三四五六七八九十]+)：", b[0]).group(1)
    print(u"  俱在｜第%s章 案例%s｜「%s」｜%d 行｜起 L%d" % (c, num, head, len(b), zpr[hit[0]][0] + 1))

# 章內案例序連貫（一、二、三…不重不跳）
seqbad = 0
for c, (a, z) in sorted(idx.items()):
    got = [cn2int(m.group(1)) for m in
           (re.match(u"#### 案例([〇零一二三四五六七八九十]+)：", l) for l in L[a:z]) if m]
    if got and got != list(range(1, len(got) + 1)):
        seqbad += 1
        print(u"  序斷｜第%s章：%s" % (c, got))
print(u"== 插入覆核｜塊 %d（缺席 %d）｜章序連貫 %d/%d 章" % (len(blocks), bad, len(idx) - seqbad, len(idx)))
