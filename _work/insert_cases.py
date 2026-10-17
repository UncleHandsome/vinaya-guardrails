# -*- coding: utf-8 -*-
"""案例插入器（通用）：讀草稿檔（以 `#CH n` 分節，一節可含數案，每案末行須為 `---`），
插入該章最後一則案例之後、下一標題之前。**同章多塊一律合併為一次插入**（分插會令章內倒序）。
用法：python -X utf8 _work/insert_cases.py <草稿檔> [--go]
自證：塊首=#### 案例、塊尾=---、末案例之隔線確在插入點前一行、案例總數增量＝草稿之案例數（非塊數）、CRLF 不變。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
D = sys.argv[1]
U = u"零一二三四五六七八九"

L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
d = io.open(D, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

blocks, cur, ch = [], None, None
for ln in d:
    if ln.startswith("#CH "):
        if cur is not None:
            blocks.append((ch, cur))
        ch, cur = int(ln[4:].strip()), []
    elif cur is not None:
        cur.append(ln)
if cur is not None:
    blocks.append((ch, cur))


def trim(x):
    while x and not x[0].strip():
        x = x[1:]
    while x and not x[-1].strip():
        x = x[:-1]
    return x


blocks = [(c, trim(b)) for c, b in blocks]
for c, b in blocks:
    assert b and b[0].startswith(u"#### 案例"), u"第%s章塊首非案例標題：%s" % (c, b[:1])
    assert b[-1].strip() == u"---", u"第%s章塊尾非隔線：%s" % (c, b[-1][:20])
print("草稿塊：%d（章：%s）" % (len(blocks), "、".join(str(c) for c, _ in blocks)))


def cn2int(s):
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s) if s else -1


CHH = re.compile(u"^# 第(.+?)章")
st = [(cn2int(m.group(1)), i) for i, l in enumerate(L) for m in [CHH.match(l)] if m]
idx = {n: (st[k][1], st[k + 1][1] if k + 1 < len(st) else len(L)) for k, n in enumerate([x[0] for x in st])}

bych = {}
for c, b in blocks:
    bych.setdefault(c, []).extend(b + [u""])
for c in bych:
    while bych[c] and not bych[c][-1].strip():
        bych[c].pop()
    bych[c].append(u"")

ins = []
ORD = re.compile(u"^#### 案例(.+?)：")
for c, b in bych.items():
    a, z = idx[c]
    cas = [i for i in range(a, z) if L[i].startswith(u"#### 案例")]
    assert cas, u"第%s章查無案例" % c
    # 序號須当场量、当场斷（第卅輪偿 #52 之債：历轮皆靠人工先量末案序， once 記錯即章內重號）
    have = [cn2int(m.group(1)) for m in (ORD.match(L[i]) for i in cas) if m]
    assert len(have) == len(cas), u"第%s章有案例標題不帶序號（『案例X：』式樣走樣）：%s" % (
        c, [L[i][:24] for i in cas if not ORD.match(L[i])])
    assert have == list(range(1, len(cas) + 1)), u"第%s章原有案序不連貫：%s" % (c, have)
    new = [cn2int(m.group(1)) for m in (ORD.match(x) for x in b if x.startswith(u"#### 案例")) if m]
    nd = sum(1 for x in b if x.startswith(u"#### 案例"))
    assert len(new) == nd, u"第%s章草稿有 %d 則案例標題不帶『案例X：』序號（式樣走樣，序號檢即失效）" % (c, nd - len(new))
    assert new == list(range(len(cas) + 1, len(cas) + 1 + len(new))), u"第%s章草稿案序應自 %d 起連貫，實為 %s" % (
        c, len(cas) + 1, new)
    last = cas[-1]
    nxt = next(i for i in range(last, z) if re.match(u"^#{1,4} ", L[i]) and i > last)
    p = nxt - 1
    while p > last and not L[p].strip():
        p -= 1
    assert L[p].strip() == u"---", u"第%s章末案例隔線不在 L%d（%s）" % (c, p + 1, L[p][:20])
    print(u"  第%s章｜原有案序 1..%d｜草稿接 %s" % (c, len(cas), u"、".join(str(x) for x in new)))
    ins.append((p + 1, c, len(cas), b))
ins.sort(reverse=True)

out = list(L)
for p, c, n, b in ins:
    out[p:p] = b
    print("  第%s章｜案例 %d→%d｜插於 L%d（+%d 行）"
          % (c, n, n + sum(1 for x in b if x.startswith(u"#### 案例")), p, len(b)))

new = u"\r\n".join(out)
assert new.count(u"\r\n") == len(out) - 1, u"CRLF 變形"
assert u"\n" not in new.replace(u"\r\n", u""), u"混入裸 LF"
b0 = sum(1 for x in L if x.startswith(u"#### 案例"))
b1 = sum(1 for x in out if x.startswith(u"#### 案例"))
ncas = sum(1 for _, b in blocks for x in b if x.startswith(u"#### 案例"))   # 一塊可含多案（同章合併為一次插入）
assert b1 == b0 + ncas, u"案例總數不合：%d→%d（應 +%d）" % (b0, b1, ncas)
if u"--go" not in sys.argv:
    print(u"（覆核模式，未寫檔；加 --go 即入書）")
    sys.exit(0)
io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
print("案例：%d→%d｜行數：%d→%d（差 %+d）" % (b0, b1, len(L), len(out), len(out) - len(L)))
