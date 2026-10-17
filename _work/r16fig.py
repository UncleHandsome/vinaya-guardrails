# -*- coding: utf-8 -*-
"""第 49 輪改圖：第一章「行為心理防禦工事圖」——單提與捨墮改為同層並列（一框兩行）。

沿用 r12fig.py 之法：生成器而非字串替換，算格・對齊・上限三斷言俱在。
格寬口徑同印面尺：CJK（U+2E80 以上）2 格，框線與半形 1 格；上限 84 格（≈10.8pt）。
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv
MAXG = 84


def gw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)

# ── 定位：第一章圍欄（含【最外層護城河】者）──
i0 = next(n for n, t in enumerate(L) if t.strip() == u"```" and any(
    u"【最外層護城河】" in L[k] for k in range(n + 1, min(n + 4, len(L)))))
i1 = next(n for n in range(i0 + 1, len(L)) if L[n].strip() == u"```")
blk = L[i0 + 1:i1]
print(u"第一章圖：L%d–L%d｜%d 行｜最寬 %d 格" % (i0 + 2, i1, len(blk), max(gw(x) for x in blk)))
assert [u"【動態預警系統】" in x for x in blk] and any(u"【物質極簡隔離】" in x for x in blk)

ARROW = u"                                  ↓"
IND = 8


def pad(s, k):
    while gw(s) < k:
        s += u" "
    assert gw(s) == k, (u"補不齐", gw(s), k, s)
    return s


hdr = u"此兩條同屬波逸提，罪質平行，無分深淺"
row1 = u"【動態預警系統】九十單提法（管身口：妄語、獨處、惡口、肢體衝突）"
row2 = u"【物質極簡隔離】三十捨墮法（管物資：衣、鉢、金錢、器物之私產囤積）"
texts = (hdr, row1, row2)
inner = max(gw(x) for x in texts) + 2                   # 框內左右各留一空格
top = IND * u" " + u"┌" + inner * u"─" + u"┐"
bot = IND * u" " + u"└" + inner * u"─" + u"┘"
mids = [IND * u" " + u"│" + pad(u" " + x, inner) + u"│" for x in texts]
new = [top] + mids + [bot]
TOT = IND + inner + 2

# ── 斷言：等寬・豎線與角同格・不超版寬・字形清白 ──
for x in new:
    assert gw(x) == TOT, (u"行寬不一", gw(x), TOT, x)
for x in new:
    assert x[IND] in (u"│", u"┌", u"└"), (u"左角未對齊", x)
    assert x[-1] in (u"│", u"┐", u"┘"), (u"右角未對齊", x)
assert TOT <= MAXG, (u"超出版寬", TOT, MAXG)
for x in new:
    assert u"・" not in x and u"/" not in x and u"**" not in x and u"「" not in x, (u"禁用字形", x)
print(u"新框：總寬 %d 格（≤%d）｜%d 行" % (TOT, MAXG, len(new)))

# ── 換入：取原三行（單提・箭頭・捨墮）以框代之，前後箭頭保留 ──
a = next(k for k, x in enumerate(blk) if u"【動態預警系統】" in x)
b = next(k for k, x in enumerate(blk) if u"【物質極簡隔離】" in x)
assert blk[a - 1].strip() == u"↓" and b == a + 2, (u"原段形不符", blk[a - 1], blk[a + 1])
old3 = blk[a:b + 1]
blk2 = blk[:a] + new + blk[b + 1:]
assert blk2[0] == blk[0] and blk2[-1] == blk[-1]
for x in blk2:
    assert gw(x) <= MAXG, (u"段內超寬", gw(x), x)
print(u"段內行數 %d → %d｜最寬 %d 格" % (len(blk), len(blk2), max(gw(x) for x in blk2)))
print(u"刪去之舊三行：")
for x in old3:
    print(u"   %r" % x)

L[i0 + 1:i1] = blk2

# ── 圖注（圍欄之後補一行）＋ 卷端術語式樣歸正 ──
j = i0 + 1 + len(blk2) + 1                      # 閉合 ``` 之下一行
assert L[j - 1].strip() == u"```" and L[j] == u"", (u"閉合界不符", L[j - 1], repr(L[j]))
NOTE = (u"（圖注：九十單提與三十捨墮在律中同屬『波逸提』——捨墮的全名便是『尼薩耆波逸提』，"
        u"兩者罪質平行，同對一位清淨比丘發露即得清淨，故此圖將兩條畫在同一層；"
        u"其別只在犯後手中有物與否。圖自上而下是敵軍攻入的方向，非罪之輕重階梯，說詳第三章。）")
L[j + 1:j + 1] = [NOTE, u""]
print(u"添圖注 @L%d" % (j + 2))

k = next(n for n, t in enumerate(L) if u"行為心理防禦工事圖" in t and u"**" in t)
assert L[k].count(u"**「行為心理防禦工事圖」**") == 1
L[k] = L[k].replace(u"**「行為心理防禦工事圖」**", u"『行為心理防禦工事圖』")
print(u"式樣歸正 @L%d（本書術語不借逐字式樣）" % (k + 1))

out = NL.join(L)
assert out.count(chr(13)) == len(L) - 1
print(u"行數 %d → %d｜CR %d" % (n0, len(L), out.count(chr(13))))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑，未寫入）")
    for x in blk2:
        print(u"  %s" % x)
