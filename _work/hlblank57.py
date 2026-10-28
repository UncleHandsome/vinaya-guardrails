# -*- coding: utf-8 -*-
"""第 57 輪・辛：印面黑塊之治——只在『被 pandoc 併段的相鄰行』之間補空行，一字不動。
病（外路第二十報，測得實情）：案例卡【案發現場】欄內，作者一行一拍，但相鄰行之間無空行，
    CommonMark 遂併為同一個 <p>——故印面出現 600–841 字之單段。上一刀按『源檔單行』計量，
    量到的是假數（單行最長 559，印面實則 841）——尺之單位錯，則綠亦非綠。
治：對『合併後 >CEIL 字』之段，於其內部每一處句末（。！？…＋閉合符）之行界補一空行；
    行本身已是完整一拍者方補，句中折行者不補（交予 pandoc 自行接排）。
自證：補行前後全檔『非空白字元』總數須一字不差・CRLF 等式・圍欄內與表格行俱不碰。
用法：python -X utf8 _work/hlblank57.py [--go]
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
CEIL = 320
raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
assert raw.count(u"\r") == raw.count(u"\n"), u"入口 CRLF 已傷"
L = raw.split(u"\r\n")
N0 = len(L)
CN = lambda s: len(re.sub(u"[^一-龥]", u"", s))
LI = re.compile(u"^\\s*(?:[*+-]|\\d+[.)])\\s+")
END = re.compile(u"[。！？…][」』）】”\"*]*\\s*$")
COLON = re.compile(u"[：:][”\"*]*\\s*$")     # 以冒號收行、下接引文者，亦是一拍之終
FENCE = u"```"


def skip(l):
    return l.startswith((u"#", u"|", u">")) or l.startswith(FENCE)


# 一、找出『印面段落』＝相鄰非空行（未被空行隔開、且非相鄰兩清單項）之併塊
paras, i, inf = [], 0, False
APX = next((n for n, l in enumerate(L) if l.startswith(u"# 附錄")), len(L))   # 附錄乃公具，不在段長口徑內（與 hlannot ④ 同）
while i < APX:
    if L[i].startswith(FENCE):
        inf = not inf
        i += 1
        continue
    if inf or not L[i].strip() or skip(L[i]):
        i += 1
        continue
    j = i + 1
    while j < APX and not inf and L[j].strip() and not skip(L[j]):
        if LI.match(L[j]):                     # 凡行首為清單符，另起一段（模型之誤已糾：編號項各自成段）
            break
        if L[j].startswith(FENCE):
            break
        j += 1
    paras.append((i, j))
    i = j
# 二、於 >CEIL 之併塊內，句末行界補空行
ins = []
for a, b in paras:
    if b - a < 2 or CN(u"".join(L[a:b])) <= CEIL:
        continue
    for k in range(a, b - 1):
        nxt = L[k + 1].lstrip()
        if not END.search(L[k]) and not (COLON.search(L[k]) and nxt.startswith((u"「", u"『"))):
            continue
        if L[k].count(u"「") > L[k].count(u"」"):   # 引號未閉，不合行（否則把一則引文鋸成兩段）
            continue
        if L[k + 1].lstrip().startswith((u"」", u"』", u"）", u"**（")):
            continue
        ins.append(k + 1)
ins = sorted(set(ins), reverse=True)
for p in ins:
    L[p:p] = [u""]
print(u"補空行 %d 處｜行數 %d→%d" % (len(ins), N0, len(L)))
txt = u"\r\n".join(L)
assert re.sub(u"[^一-龥]", u"", txt) == re.sub(u"[^一-龥]", u"", raw), u"漢字有損"
assert txt.count(u"\r") == txt.count(u"\n"), u"出口 CRLF 變形"
# 三、重量印面段落
L2 = txt.split(u"\r\n")
APX2 = next((n for n, l in enumerate(L2) if l.startswith(u"# 附錄")), len(L2))
p2, i, inf = [], 0, False
while i < APX2:
    if L2[i].startswith(FENCE):
        inf = not inf
        i += 1
        continue
    if inf or not L2[i].strip() or skip(L2[i]):
        i += 1
        continue
    j = i + 1
    while j < APX2 and not inf and L2[j].strip() and not skip(L2[j]):
        if LI.match(L2[j]):
            break
        if L2[j].startswith(FENCE):
            break
        j += 1
    p2.append((CN(u"".join(L2[i:j])), i + 1))
    i = j
p2.sort(reverse=True)
print(u"補後印面段落 %d 段｜>320 字 %d 段｜最長 %d 字（L%d）" % (
    len(p2), sum(1 for c, _n in p2 if c > CEIL), p2[0][0], p2[0][1]))
for c, n in p2[:8]:
    print(u"   %4d 字 L%-5d %s" % (c, n, re.sub(u"[*\\s]", u"", L2[n - 1])[:22]))
if u"--go" in sys.argv:
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已寫檔")
else:
    print(u"（乾跑：加 --go 始寫）")
