# -*- coding: utf-8 -*-
"""宣稱對實測：逐章取「精選／選取 N 條（個／組／幕／則）」句，與該章 `#### 案例` 實數比對。
   此尺為第 6 輪之教而設：補案後宣稱必落後，而目錄與正文之數已由 sync_toc 斷言，唯此類修辭句無尺照管。
用法：python -X utf8 _work/claimchk.py
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
U = u"零一二三四五六七八九"
L = io.open(BOOK, encoding="utf-8", newline="").read().split("\r\n")


def cn2int(s):
    if u"百" in s:
        a, b = s.split(u"百", 1)
        v = (U.index(a) if a else 1) * 100
        return v + (cn2int(b) if b and b != u"零" else 0)
    if s == u"十":
        return 10
    if s.startswith(u"廿"):
        return 20 + (U.index(s[1]) if len(s) > 1 else 0)
    if s.startswith(u"十"):
        return 10 + U.index(s[1])
    if u"十" in s:
        a, b = s.split(u"十")
        return U.index(a) * 10 + (U.index(b) if b else 0)
    return U.index(s)


CHH = re.compile(u"^# 第(.+?)章")
st = [(cn2int(m.group(1)), i) for i, l in enumerate(L) for m in [CHH.match(l)] if m]
idx = {n: (st[k][1], st[k + 1][1] if k + 1 < len(st) else len(L)) for k, n in enumerate([x[0] for x in st])}
# 動詞與數詞之間可有修飾語（「精選其中最具代表性的十五條戒律」）——舊式樣只認緊接之數，
# 遂漏管第七・第八章兩處宣稱（外審報告逮到，實為本尺之盲點，非書無據）。
CLAIM = re.compile(u"(精選|選取|挑選)([^。；，、]{0,16}?)"
                   u"([〇零一二三四五六七八九十廿]{1,4})\\s*(條|個|組|則|幕|案)")
# 另有以「以下／現場的／再取」起手的宣稱句（第11章：「制度現場的廿三幕」；第10章：「此處再取五則」
# ——后者之病正在導言計數落後於實數，外審第卅六輪即因此案而中），無動詞可認，
# 舊式樣遂全數漏管——補一式樣，只認緊接之數，免把修飾語裡的數字誤當宣稱。
CLAIM2 = re.compile(u"(以下|現場的|再取)([〇零一二三四五六七八九十廿]{1,4})\\s*(幕|案|則|條)")

n_ok = n_bad = n_noclaim = 0
for c, (a, z) in sorted(idx.items()):
    real = sum(1 for x in L[a:z] if x.startswith(u"#### 案例"))
    got = []
    for i in range(a, z):
        for m in CLAIM.finditer(L[i]):
            if u"案例" in L[i] or u"戒" in L[i] or u"因緣" in L[i] or u"條目" in L[i]:
                got.append((i + 1, m.group(3), m.group(4), L[i].strip()[:64]))
        for m in CLAIM2.finditer(L[i]):
            got.append((i + 1, m.group(2), m.group(3), L[i].strip()[:64]))
    if not got:
        n_noclaim += 1
        continue
    for ln, num, unit, txt in got:
        v = cn2int(num)
        tag = u"✓" if v == real else u"✗"
        if v == real:
            n_ok += 1
        else:
            n_bad += 1
        print(u"%s 第%-3d章｜宣稱 %s%s｜實測案例 %d｜L%d｜%s" % (tag, c, num, unit, real, ln, txt))
print(u"== 宣稱 %d 條相符、%d 條不符｜無宣稱之章 %d" % (n_ok, n_bad, n_noclaim))

# 跨章之宣稱（第卅七輪之教：地圖導言手打「一百六十三則案例」，正文屆已 164——章級之尺照不到
# 通盤之數，故另立兩式：全書案例總數、地圖「重排N遍」對其小節實數。先量過：全書式樣唯 1 命中，無假陽性）
TOTAL = sum(1 for x in L if x.startswith(u"#### 案例"))
CLAIM3 = re.compile(u"(全書|本書)([〇零一二三四五六七八九十百廿]{1,6})則")
CLAIM4 = re.compile(u"重排([〇零一二三四五六七八九十百廿]{1,4})遍")
MSTART = [i for i, s in enumerate(L) if s.startswith(u"# 十線地圖")]
SECRUN = re.compile(u"^## [〇零一二三四五六七八九十]+、")
n_map = 0
if MSTART:
    a = MSTART[0]
    z = next((j for j in range(a + 1, len(L)) if L[j].startswith(u"# ")), len(L))
    n_map = sum(1 for s in L[a:z] if SECRUN.match(s))
n3 = 0
for i, s in enumerate(L):
    for m in CLAIM3.finditer(s):
        v = cn2int(m.group(2))
        n3 += 1
        print(u"%s 全書案例｜宣稱 %s則｜實測 %d｜L%d" % (u"✓" if v == TOTAL else u"✗", m.group(2), TOTAL, i + 1))
        if v != TOTAL:
            n_bad += 1
    for m in CLAIM4.finditer(s):
        v = cn2int(m.group(1))
        n3 += 1
        print(u"%s 地圖重排｜宣稱 %s遍｜小節實測 %d｜L%d" % (u"✓" if v == n_map else u"✗", m.group(1), n_map, i + 1))
        if v != n_map:
            n_bad += 1
print(u"== 跨章宣稱 %d 條｜全書案例 %d 則｜地圖小節 %d｜累計不符 %d" % (n3, TOTAL, n_map, n_bad))

