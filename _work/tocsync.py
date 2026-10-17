# -*- coding: utf-8 -*-
"""目錄覆蓋器：目錄之案例項與節項，一律以正文標題為準重建（單一法源）。
別式（掛在含『案例』之節題下的主題名）亦歸前式「案例N：〈正文題〉」，使全書目錄體例畫一。
硬斷言：每章覆蓋後，目錄案例項數須等於正文「#### 案例」數；行數變化須等於 0。
用法：python -X utf8 _work/tocsync.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOOK = HP.SRC
U = u"零一二三四五六七八九十"
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"CRLF 已傷"
L = raw.split(u"\r\n")
N0 = len(L)


def cn2int(s):
    if len(s) == 1:
        return U.index(s)
    if s.startswith(u"十"):
        return 10 + (U.index(s[1]) if len(s) == 2 else 0)
    if len(s) == 3 and s[1] == u"十":
        return U.index(s[0]) * 10 + U.index(s[2])
    if s.endswith(u"十"):
        return U.index(s[0]) * 10
    return None


CHAP = re.compile(u"^# 第([一二三四五六七八九十]{1,3})章")
TOCH = re.compile(u"^\\* \\*\\*第([一二三四五六七八九十]{1,3})章")
toc0 = next(i for i, l in enumerate(L) if u"【全書詳細目錄】" in l)
toc1 = next(i for i in range(toc0 + 1, len(L)) if CHAP.match(L[i]))

# 正文之案例題與節題
bc, bs = {}, {}
cur = None
for i, l in enumerate(L):
    m = CHAP.match(l)
    if m:
        cur = cn2int(m.group(1))
        bc[cur], bs[cur] = [], []
        continue
    if cur is None or i < toc1:
        continue
    m = re.match(u"^#### (案例[一二三四五六七八九十]+)：(.*)$", l)
    if m:
        bc[cur].append((m.group(1), m.group(2).strip()))
        continue
    m = re.match(u"^### ([一二三四五六七八九十]+)、\\s*(.*)$", l)
    if m:
        bs[cur].append((m.group(1), m.group(2).strip()))

tst = sorted([(cn2int(TOCH.match(L[i]).group(1)), i) for i in range(toc0, toc1) if TOCH.match(L[i])])
tsp = {t[0]: (t[1], tst[k + 1][1] if k + 1 < len(tst) else toc1) for k, t in enumerate(tst)}
nch_c = nch_s = 0
for c in sorted(tsp):
    a, z = tsp[c]
    # 一、案例項（前式）
    rows = [(i, m.group(1), m.group(2), m.group(3)) for i in range(a, z)
            for m in [re.match(u"^(\\s*\\*\\s*)(案例[一二三四五六七八九十]+)：(.*)$", L[i])] if m]
    if len(rows) != len(bc[c]):
        # 二、別式：找含『案例』之節題，其下更深一層之連列即目錄之案例項
        anchor, ain = None, 0
        for i in range(a, z):
            m = re.match(u"^(\\s*)\\*\\s*[一二三四五六七八九十]+、", L[i])
            if m and u"案例" in L[i]:
                anchor, ain = i, len(m.group(1))
        kill = []
        if anchor is not None:
            j = anchor + 1
            while j < z:
                m = re.match(u"^(\\s*)\\*\\s*", L[j])
                if not m or len(m.group(1)) <= ain:
                    break
                if re.match(u"^\\s*\\*\\s*案例[一二三四五六七八九十]+：", L[j]):
                    break
                kill.append(j)
                j += 1
        assert len(kill) == len(bc[c]), u"第%s章別式案例項 %d／正文 %d 不合，不敢擅動" % (c, len(kill), len(bc[c]))
        new = [u" " * (ain + 2) + u"* %s：%s" % (k, t) for k, t in bc[c]]
        print(u"  第%s章｜別式 %d 行 → 前式 %d 行（L%d）" % (c, len(kill), len(new), kill[0] + 1))
        L[kill[0]:kill[-1] + 1] = new
        nch_c += len(new)
        z = z + len(new) - len(kill)
        rows = [(i, m.group(1), m.group(2), m.group(3)) for i in range(a, z)
                for m in [re.match(u"^(\\s*\\*\\s*)(案例[一二三四五六七八九十]+)：(.*)$", L[i])] if m]
    assert len(rows) == len(bc[c]), u"第%s章目錄案例項 %d／正文 %d 不合" % (c, len(rows), len(bc[c]))
    for (i, pre, kn, oldt), (bkn, bt) in zip(rows, bc[c]):
        if oldt.strip() == bt:
            continue
        L[i] = pre + u"%s：%s" % (bkn, bt)
        nch_c += 1
        print(u"    L%-5d %s｜%s" % (i + 1, bkn, bt[:60]))
    # 三、節項
    srows = [(i, m.group(1), m.group(2), m.group(3)) for i in range(tsp[c][0], tsp[c][1])
             for m in [re.match(u"^(\\s*\\*\\s*)([一二三四五六七八九十]+)、\\s*(.*)$", L[i])] if m]
    assert len(srows) == len(bs[c]), u"第%s章目錄節項 %d／正文 %d 不合" % (c, len(srows), len(bs[c]))
    for (i, pre, kn, oldt), (bkn, bt) in zip(srows, bs[c]):
        if kn != bkn:
            print(u"    ✗ 第%s章 目錄節『%s、』對不上正文『%s、』" % (c, kn, bkn))
            continue
        if oldt.strip() == bt:
            continue
        L[i] = pre + u"%s、 %s" % (bkn, bt)
        nch_s += 1
        print(u"    L%-5d %s、%s" % (i + 1, bkn, bt[:56]))
print(u"覆蓋：案例項 %d 行｜節項 %d 行｜行數 %d→%d" % (nch_c, nch_s, N0, len(L)))
assert len(L) == N0, u"行數變形"
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n"), u"CRLF 變形"
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"覆核模式（未寫檔）")
