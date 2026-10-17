# -*- coding: utf-8 -*-
"""目錄與宣稱同步器（通用，第三版）：目錄條目兩種式樣皆認——
    前式「    * 案例一：…」；別式（掛在含「案例」之節題下）「    * 大摶飯與嚼飯作聲：…」。
同步檔每行可帶或不帶「* 」前綴，一律只取正文，縮排與式樣由本章目錄自定。格式——
    #TOC <章序>
    <目录条目正文>…
    #CLAIM
    <舊句>→<新句>…
    #END
硬斷言：插入後該章「目錄案例項數」必須等於該章正文「#### 案例」數（不符即中止，不寫檔）。
用法：python -X utf8 _work/sync_toc.py <同步檔> [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
U = u"零一二三四五六七八九"
lines_all = io.open(sys.argv[1], encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")

want, claims, key = {}, [], None
for ln in lines_all:
    s = ln.rstrip()
    if s.startswith("#TOC "):
        key = ("toc", int(s[5:].strip()))
        want[key[1]] = []
    elif s.strip() == "#CLAIM":
        key = ("claim", None)
    elif s.strip() in ("#END",):
        key = None
    elif key and key[0] == "toc" and s.strip():
        want[key[1]].append(re.sub(u"^\\*\\s*", u"", s.strip()))
    elif key and key[0] == "claim" and u"→" in s:
        a, b = s.split(u"→", 1)
        claims.append((a.strip(), b.strip()))
print("同步檔解析：目錄 %s｜宣稱 %d 對" % (
    "、".join("%s章×%d行" % (k, len(v)) for k, v in sorted(want.items())), len(claims)))
assert all(v for v in want.values()), u"有章別目錄行為空——同步檔未正確解析"


def toc_cas(lines, a, z):
    """本章目錄之案例條目行號。前式直接認「* 案例」；別式認含「案例」節題下之同層連列。"""
    pref = [i for i in range(a, z) if lines[i].startswith(u"    * 案例")]
    if pref:
        return pref
    for i in range(a, z):
        if lines[i].startswith(u"  * ") and u"案例" in lines[i]:
            j = i + 1
            while j < z and lines[j].startswith(u"    * "):
                j += 1
            if j > i + 1:
                return list(range(i + 1, j))
    return []


def cn_order(s):
    if s == u"十":
        return 10
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s)


GO = "--go" in sys.argv
L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")
toc0 = next(i for i, l in enumerate(L) if u"【全書詳細目錄】" in l)
toc1 = next(i for i in range(toc0 + 1, len(L)) if re.match(u"^# 第.+章", L[i]))
HEAD = re.compile(u"^\\* \\*\\*第(.+?)章")
CHH = re.compile(u"^# 第(.+?)章")

tst = sorted([(cn_order(HEAD.match(L[i]).group(1)), i) for i in range(toc0, toc1) if HEAD.match(L[i])])
tspan = {n: (tst[j][1], tst[j + 1][1] if j + 1 < len(tst) else toc1) for j, n in enumerate([x[0] for x in tst])}
bst = sorted([(cn_order(CHH.match(L[i]).group(1)), i) for i, l in enumerate(L) for m in [CHH.match(l)] if m])
bspan = {n: (bst[j][1], bst[j + 1][1] if j + 1 < len(bst) else len(L)) for j, n in enumerate([x[0] for x in bst])}

out = list(L)
ins = []
for c, add in sorted(want.items()):
    a, z = tspan[c]
    tc = toc_cas(L, a, z)
    assert tc, u"第%s章目錄無案例項" % c
    print("  第%s章目錄式樣：%s" % (c, u"前式（案例N：）" if L[tc[0]].startswith(u"    * 案例") else u"別式（節題下列名）"))
    ins.append((tc[-1] + 1, c, len(tc), [u"    * " + b for b in add]))
ins.sort(reverse=True)
for p, c, n, add in ins:
    out[p:p] = add
    print("  目錄第%s章｜案例項 %d→%d｜插於 L%d" % (c, n, n + len(add), p + 1))

# 覆核：以插入後之檔重新定位（舊窗會溢入鄰章，數出虛高）
nl = out
n2 = len(nl)
t0 = next(i for i, l in enumerate(nl) if u"【全書詳細目錄】" in l)
t1 = next(i for i in range(t0 + 1, n2) if re.match(u"^# 第.+章", nl[i]))
st2 = sorted([(cn_order(HEAD.match(nl[i]).group(1)), i) for i in range(t0, t1) if HEAD.match(nl[i])])
ts2 = {n: (st2[j][1], st2[j + 1][1] if j + 1 < len(st2) else t1) for j, n in enumerate([x[0] for x in st2])}
bs2 = sorted([(cn_order(CHH.match(nl[i]).group(1)), i) for i, l in enumerate(nl) for m in [CHH.match(l)] if m])
bd2 = {n: (bs2[j][1], bs2[j + 1][1] if j + 1 < len(bs2) else n2) for j, n in enumerate([x[0] for x in bs2])}
bad = []
for c in sorted(want):
    a, z = ts2[c]
    tn = len(toc_cas(nl, a, z))
    ba, bz = bd2[c]
    bn = sum(1 for i in range(ba, bz) if nl[i].startswith(u"#### 案例"))
    print("  覆核第%s章｜目錄 %d／正文 %d" % (c, tn, bn))
    if tn != bn:
        bad.append((c, tn, bn))
assert not bad, u"目錄與正文案例數不合：%s" % bad

txt = u"\r\n".join(out)
for a, b in claims:
    n = txt.count(a)
    assert n == 1, u"宣稱命中 %d（應 1）：%s" % (n, a[:28])
    txt = txt.replace(a, b)
    print("  宣稱｜%s → %s" % (a[:20], b[:20]))
assert txt.count(u"\r\n") == len(txt.split(u"\r\n")) - 1, u"CRLF 變形"
print("行數：%d→%d｜%s" % (len(L), len(nl), "寫檔" if GO else "覆核模式（未寫檔）"))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(txt)
