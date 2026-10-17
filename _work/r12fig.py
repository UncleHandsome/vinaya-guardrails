# -*- coding: utf-8 -*-
"""第 45 輪・第三章同心圓圖改版（作者令「要改圖」）。
   中段（第四重・九十單提／第三重・三十捨墮）由上下兩行改為同深之左右兩欄；
   框下加一行圖內自註：「此兩欄同屬波逸提，罪質平行，無分深淺」。
   五重之名與層級語一律不動；圖注之「圖上之內外」改「圖上之左右」。
   以格寬模型生成每一行，斷全段等寬、分隔欄上下對齊、無日式中黑、無逐字式樣。
用法：python -X utf8 _work/r12fig.py [--go]"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import sys

BOOK = HP.SRC


def gw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


def pad(s, w):
    g = gw(s)
    assert g <= w, u"格寬溢出：%s（%d＞%d）" % (s, g, w)
    return s + u" " * (w - g)


def gcol(s, target):
    """回傳第 target 格處之字元（以格寬模型定位）。"""
    acc = 0
    for c in s:
        if acc == target:
            return c
        acc += 2 if ord(c) > 0x2E80 else 1
    return u""


raw = io.open(BOOK, encoding="utf-8", newline=u"").read()
L = raw.split(u"\r\n")
i5 = next(i for i, s in enumerate(L) if s.startswith(u"│ 第五重"))
i1 = next(i for i, s in enumerate(L) if s.startswith(u"│ 第一重"))
top, bot = i5 - 1, i1 + 1
assert L[top].startswith(u"┌") and L[bot].startswith(u"└"), u"框界不對"
assert any(s.startswith(u"│ 第四重") for s in L[top:bot + 1]), u"圖中無第四重之行"
print(u"圖段：L%d–L%d（%d 行）" % (top + 1, bot + 1, bot - top + 1))

CW, LINE = 30, u"─"
FULL = 2 * CW + 1
BAR, TEE, ELB, CRT, TUP = u"│", u"├", u"┤", u"┬", u"┴"


def frow(txt):
    return BAR + u" " + pad(txt, FULL - 1) + BAR


def srow(a, b):
    return BAR + u" " + pad(a, CW - 1) + BAR + u" " + pad(b, CW - 1) + BAR


def sep(mid):
    return TEE + LINE * CW + mid + LINE * CW + ELB


D = u"──"
NEW = [
    u"┌" + LINE * FULL + u"┐",
    frow(u"第五重：外圍護城河與斥候哨所 " + D + u" 百眾學法、四提舍尼法"),
    sep(CRT),
    srow(u"第四重：外城牆與動態警戒陣地", u"第三重：物資軍械管制與內城門"),
    srow(D + u" 九十單提法", D + u" 三十捨墮法"),
    sep(TUP),
    frow(u"第二重：皇城宮牆與加護救治所 " + D + u" 十三僧殘法"),
    TEE + LINE * FULL + ELB,
    frow(u"第一重：國王的心臟與修道生命 " + D + u" 四大波羅夷（根本性戒）"),
    u"└" + LINE * FULL + u"┘",
    u"        ↑ 此兩欄同屬波逸提，罪質平行，無分深淺 ↑",
]
for s in NEW:
    assert u"・" not in s and u"**" not in s and u"「" not in s, u"雜質：" + s
box = [s for s in NEW if s.startswith(BAR)]
assert len(set(gw(s) for s in box)) == 1, u"框內行格寬不一：%s" % sorted(set(gw(s) for s in box))
W = gw(NEW[0])
assert W <= 84, u"全寬 %d 格逾 10.8pt 之上限" % W
split = [i for i, s in enumerate(NEW) if s.startswith(BAR) and s.count(BAR) == 3]
assert len(split) == 2, u"分欄行數異常"
off = 1 + CW
assert all(gcol(s, off) == BAR for s in NEW[split[0]:split[1] + 1]), u"分欄豎線不對齊"
assert gcol(NEW[2], off) == CRT and gcol(NEW[5], off) == TUP, u"分欄起止之丁字不對齊"
print(u"新段全寬 %d 格（原 60）｜%d 行｜字級估算 %.2fpt" % (W, len(NEW), 505.0 / (0.55 * W)))
for s in NEW:
    print(u"  %s（%d）" % (s, gw(s)))

tz_old = u"圖上之內外，分的是管物與管身口兩種職務"
tz_new = u"圖上之左右，分的是管身口與管物兩種職務"
assert sum(tz_old in s for s in L) == 1, u"圖注錨命不同"
print(u"圖注：「圖上之內外」→「圖上之左右」✓")
if u"--go" in sys.argv:
    L[top:bot + 1] = NEW
    for i, s in enumerate(L):
        if tz_old in s:
            L[i] = s.replace(tz_old, tz_new)
    txt = u"\r\n".join(L)
    assert txt.count(u"\r\n") == len(L) - 1, u"CRLF 變形"
    io.open(BOOK, "w", encoding="utf-8", newline=u"").write(txt)
    print(u"已改檔｜全檔 %d 行" % len(L))
else:
    print(u"未改（加 --go）")
