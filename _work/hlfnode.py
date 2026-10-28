# -*- coding: utf-8 -*-
"""節點對合尺（hlfnode）：源檔圍欄之柵行・箭頭行・豎線行格位對合明細。逐段列出柵行・箭頭行・豎線行之格位，判两类之病：
   甲＝箭頭（▼↓↑→）或收攏之豎線（│）之列落於相鄰柵行之『橫 span 之外』（真懸空，不附於任何線）；
   丙＝欄內豎線切過內文（其列之左右皆有漢字，非界線）。
口徑之正（第 57 輪之教）：初版曾以『必與 ┬┴ 節點同格』為律，遂紅十二段——實則 ▼ 懸於 continuous
   ─ 線之下、│ 立於 ─ 線之上，印面即以為附著，不須另開節點（段7・段16 目視 p85/p242 俱然）。
   故判據只問『在橫 span 之內與否』；『未與節點同格』另列為備註，不視為病。
治法：甲丙須重排該圖（如段5）；純空格・框線之位移不動內文。
用法：python -X utf8 _work/hlfnode.py [段序 ...]
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "_print"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import build_hulan as BH                              # noqa: E402

RAIL = u"┌┐└┘┬┴┼│╱"
HOR = u"─═"
ARR = u"▼▲↑↓→←"
lines = io.open(BH.SRC, encoding="utf-8", newline=u"").read().split(u"\r\n")
blocks = BH.fence_blocks(lines)
KS = [int(x) for x in sys.argv[1:]] or list(range(1, len(blocks) + 1))


def cols(s, chars):
    out, g = [], 0
    for c in s:
        if c in chars:
            out.append(g)
        g += 2 if ord(c) > 0x2E80 else 1
    return out


def char_at(s, g):
    i, gg = 0, 0
    while i < len(s):
        w = 2 if ord(s[i]) > 0x2E80 else 1
        if gg == g:
            return s[i]
        if gg > g:
            return u"½"          # 落於寬字之次格（半格）
        gg += w
        i += 1
    return u" "


for k in KS:
    b = blocks[k - 1]
    hor = [i for i, x in enumerate(b) if any(c in HOR for c in x)]
    if not hor:
        print(u"段%-3d 無柵行（純列表圖）" % k)
        continue
    top, bot = hor[0], hor[-1]
    tn = cols(b[top], RAIL)
    bn = cols(b[bot], RAIL)
    arr = [(i, cols(b[i], ARR)) for i in range(len(b)) if cols(b[i], ARR)]
    vrt = [(i, cols(b[i], u"│")) for i in range(len(b)) if cols(b[i], u"│")]
    prob, note = [], []
    def span(row):
        cs = [g for g in range(BH.cw_units(b[row])) if char_at(b[row], g) in HOR + RAIL]
        return (min(cs), max(cs)) if cs else (0, 0)
    for i, cs in arr:
        if i in (top + 1, bot + 1) and cs:
            lo, hi = span(top if i == top + 1 else bot)
            out = [c for c in cs if not (lo <= c <= hi)]
            if out:
                prob.append(u"甲：L%d 箭頭出柵之外 %s（span %d–%d）" % (i + 1, out, lo, hi))
            off = [c for c in cs if c not in (tn if i == top + 1 else bn)]
            if off:
                note.append(u"L%d 箭頭 %s 未與節點同格（附於橫線，不病）" % (i + 1, off))
    for i, cs in vrt:
        if i == bot - 1 and cs:
            lo, hi = span(bot)
            out = [c for c in cs if not (lo <= c <= hi)]
            if out:
                prob.append(u"乙：L%d 豎線出柵之外 %s（span %d–%d）" % (i + 1, out, lo, hi))
        for c in cs:
            l = char_at(b[i], c - 1)
            r = char_at(b[i], c + 1)
            if l not in u" ½" and r not in u" ½":
                prob.append(u"丙：L%d 豎線@%d 切內文（左 %r 右 %r）" % (i + 1, c, l, r))
                break
    print(u"段%-3d %2d 行・%2d 格｜柵上 %s｜柵下 %s｜%s" % (
        k, len(b), max(BH.cw_units(x) for x in b), tn, bn,
        u"✓ 俱附" if not prob else u"／".join(prob)))
    for z in prob:
        print(u"      %s" % z)
