# -*- coding: utf-8 -*-
"""目錄覆蓋器：目錄之案例項與節項，一律以正文標題為準重建（單一法源）。
別式（掛在含『案例』之節題下的主題名）亦歸前式「案例N：〈正文題〉」，使全書目錄體例畫一。
第 67 輪之改：換章而案例『多寡亦變』時（6→5），舊器只敢整數對整數地換，遂擲「不敢擅動」而
    逼人一章一器（hltoc57/65/66 三支抄本）。今改為取該節下之連列整塊重建，行數之變須等於
    重建之差額（ndelta）——多寡任其變，變處須可歸；器自此一支就夠。
硬斷言：每章覆蓋後，目錄案例項數須等於正文「#### 案例」數；行數之變須等於重建差額。
用法：python -X utf8 _work/tocsync.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import hlpara  # noqa: E402  共器：中間層之形（LAYER）與 `hlchk` 丙軸同法源

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

# 正文之案例題・節題與中間層（bseq 記其原序，重建目錄時階層須照搬）
# btree 另記『節→其下之中間層與案例』之樹：69 輪換章時節數亦變（7→8）且案例分屬兩節，
#        故重建須以樹為凭，不能只把案例整塊塞進最後那個含『案例』之節。
bc, bs, bseq, btree = {}, {}, {}, {}
cur = None
for i, l in enumerate(L):
    m = CHAP.match(l)
    if m:
        cur = cn2int(m.group(1))
        bc[cur], bs[cur], bseq[cur], btree[cur] = [], [], [], []
        continue
    if cur is None or i < toc1:
        continue
    m = re.match(u"^#### (案例[一二三四五六七八九十]+)：(.*)$", l)
    if m:
        bc[cur].append((m.group(1), m.group(2).strip()))
        bseq[cur].append((u"c", m.group(1), m.group(2).strip()))
        if btree[cur]:
            btree[cur][-1][2].append((u"c", m.group(1), m.group(2).strip()))
        continue
    if l.startswith(u"### ") and re.match(hlpara.LAYER, l[4:]):
        bseq[cur].append((u"L", None, l[4:].strip()))
        if btree[cur]:
            btree[cur][-1][2].append((u"L", None, l[4:].strip()))
        continue
    m = re.match(u"^### ([一二三四五六七八九十]+)、\\s*(.*)$", l)
    if m:
        bs[cur].append((m.group(1), m.group(2).strip()))
        btree[cur].append([m.group(1), m.group(2).strip(), []])


def toc_bounds():
    """每次動完目錄都重掃章節界——行數可變，預存之界會漏看下一章之節項（68 輪之教）。
       69 輪改全檔重掃時埋一雷：正文之『* **第十二章：** 我們穿透了…』列點也合 TOCH 之形，
       遂在 L4976 後多出四枚假章條、把第十四章之界算到正文裡去。故掃攪須止於正文第一枚 H1。"""
    t1 = next((i for i in range(toc0 + 1, len(L)) if CHAP.match(L[i])), len(L))
    st = sorted([(cn2int(TOCH.match(L[i]).group(1)), i) for i in range(toc0, t1) if TOCH.match(L[i])])
    return {t[0]: (t[1], st[k + 1][1] if k + 1 < len(st) else t1) for k, t in enumerate(st)}, t1


tsp, toc1 = toc_bounds()
nch_c = nch_s = ndelta = 0
for c in sorted(tsp):
    a, z = tsp[c]
    # 〇、節數亦變（換章而節之多寡易，且案例分屬數節）：整章之節塊依 btree 重建。
    #     重建只碰『第一節行至其最後子行』，故章前之部題與空行一概不動。
    def sec_rows(a, z):
        return [(i, m.group(1), m.group(2), m.group(3)) for i in range(a, z)
                for m in [re.match(u"^(\\s*\\*\\s*)([一二三四五六七八九十]+)、\\s*(.*)$", L[i])] if m]
    srows = sec_rows(a, z)
    if len(srows) != len(bs[c]):
        assert srows, u"第%s章目錄無節項，無從重建" % c
        ain = len(L[srows[0][0]]) - len(L[srows[0][0]].lstrip())
        last = srows[0][0]
        for i in range(srows[0][0], z):
            s = L[i].strip()
            if not s:
                assert i > last, u"第%s章節塊內有空行，形制不认得，不敢擅動" % c
                continue
            ind = len(L[i]) - len(L[i].lstrip())
            if ind >= ain and s.startswith(u"* "):
                last = i
            else:
                break
        kids_c = sum(1 for _n, _t, k in btree[c] for x in k if x[0] == u"c")
        assert kids_c == len(bc[c]), u"第%s章案例 %d 則中有 %d 則不隸任何節，不敢整塊重建" % (
            c, len(bc[c]), len(bc[c]) - kids_c)
        new = []
        for num, title, kids in btree[c]:
            new.append(u" " * ain + u"* %s、 %s" % (num, title))
            under = False
            for kind, knum, text in kids:
                if kind == u"L":
                    new.append(u" " * (ain + 2) + u"* **" + text + u"**")
                    under = True
                else:
                    new.append(u" " * (ain + 4 if under else ain + 2) + u"* %s：%s" % (knum, text))
        gone = [L[i].strip()[2:] for i in range(srows[0][0], last + 1) if L[i].strip()
                and not re.match(u"^\\s*\\*\\s*[一二三四五六七八九十]+、", L[i])
                and not re.match(u"^\\s*\\*\\s*(案例[一二三四五六七八九十]+：|\\*\\*【)", L[i])]
        blanks = sum(1 for i in range(srows[0][0], last + 1) if not L[i].strip())
        print(u"  第%s章｜節塊重建：%d 行 → %d 行（節 %d／正文 %d・案例 %d 分屬 %s・別式主題名除 %d 行・夾空行 %d）" % (
            c, last - srows[0][0] + 1, len(new), len(srows), len(bs[c]), len(bc[c]),
            u"/".join(str(len([x for x in k if x[0] == u"c"])) for _n, _t, k in btree[c]),
            len(gone), blanks))
        for g in gone:
            print(u"      除：%s" % g[:74])
        L[srows[0][0]:last + 1] = new
        ndelta += len(new) - (last - srows[0][0] + 1)
        nch_s += len(new)
        nch_c += sum(1 for x in new if u"案例" in x[:12])
        tsp, toc1 = toc_bounds()
        a, z = tsp[c]
    # 一、案例項（前式）
    rows = [(i, m.group(1), m.group(2), m.group(3)) for i in range(a, z)
            for m in [re.match(u"^(\\s*\\*\\s*)(案例[一二三四五六七八九十]+)：(.*)$", L[i])] if m]
    if len(rows) != len(bc[c]):
        # 二、數亦變（換章而案例多寡易也）：取該『含案例之節題』下更深一層之連列整塊重建——
        #     前式（『* 案例N：…』）與別式（掛主題名）俱走此路，故不必再另寫一次性之目錄重建器。
        anchor, ain = None, 0
        for i in range(a, z):
            m = re.match(u"^(\\s*)\\*\\s*[一二三四五六七八九十]+、", L[i])
            if m and u"案例" in L[i]:
                anchor, ain = i, len(m.group(1))
        assert anchor is not None, u"第%s章 目錄無『含案例之節題』，不敢擅動" % c
        kill = []
        j = anchor + 1
        while j < z:
            m = re.match(u"^(\\s*)\\*\\s*", L[j])
            if not m or len(m.group(1)) <= ain:
                break
            kill.append(j)
            j += 1
        assert kill, u"第%s章 該節之下無連列，無從重建" % c
        assert kill[-1] - kill[0] + 1 == len(kill), u"第%s章 案例之列不連：%s" % (c, kill)
        # 中間層須照搬（『* **【第N樞紐…】**』縮二、其下案例縮四）——68 輪首版整塊壓平，
        # 遂把 57/65/66 三章之中間層抹掉；今依正文原序重建，階層不失。
        pre1, pre2 = u" " * (ain + 2), u" " * (ain + 4)
        new, under = [], False
        for kind, knum, text in bseq[c]:
            if kind == u"L":
                new.append(pre1 + u"* **" + text + u"**")
                under = True
            else:
                new.append((pre2 if under else pre1) + u"* %s：%s" % (knum, text))
        print(u"  第%s章｜目錄案例之列 %d 行 → 正文 %d 行（L%d..L%d，中間層 %d 條照搬）" % (
            c, len(kill), len(new), kill[0] + 1, kill[-1] + 1,
            sum(1 for k, _n, _t in bseq[c] if k == u"L")))
        L[kill[0]:kill[-1] + 1] = new
        nch_c += len(new)
        ndelta += len(new) - len(kill)
        tsp, toc1 = toc_bounds()               # 行數已變：本章與後來各章之界一律重掃
        a, z = tsp[c]
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
print(u"覆蓋：案例項 %d 行｜節項 %d 行｜行數 %d→%d（增減唯由節塊與案例之列重建，凡 %+d 行）" % (
    nch_c, nch_s, N0, len(L), ndelta))
assert len(L) - N0 == ndelta, u"行數之變出於意外：%d-%d≠%d" % (len(L), N0, ndelta)
txt = u"\r\n".join(L)
assert txt.count(u"\r") == txt.count(u"\n"), u"CRLF 變形"
if u"--go" in sys.argv:
    if txt == raw:
        print(u"檔未變，不寫（亦不備份）")
    else:
        _tag = next((a.split(u"=", 1)[1] for a in sys.argv if a.startswith(u"--tag=")), u"toc")
        BK = HP.bakpath(_tag)
        with open(BK, "wb") as fh:                     # 今制：寫正本者必先備份於 `_archive/備份/護欄/`
            fh.write(raw.encode("utf-8"))
        with open(BOOK, "wb") as fh:                    # 二進位寫：免 text 模式之 newline 雙譯
            fh.write(txt.encode("utf-8"))
        _chk = io.open(BOOK, "rb").read().decode("utf-8")
        print(u"已寫檔｜備份 %s｜回讀%s" % (
            os.path.relpath(BK, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            u"全等" if _chk == txt else u"不等!"))
        assert _chk == txt, u"回讀不等"
else:
    print(u"覆核模式（未寫檔）")
