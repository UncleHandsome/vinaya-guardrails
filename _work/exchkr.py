# -*- coding: utf-8 -*-
"""嘆號密度尺（exchkr）：只量「引號外」之感嘆號——引號內多為律文原話（「咄！男子！」之類），不較。
   口徑：以『印面段落』為一段（模型取共器 _work/hlpara.py，與段長之尺・補空行之刀同源）；
        標題／表格／引框各行自成一段（印面上各自獨立）；圍欄圖不計。一段之內引號外之「！」至多一枚（首見留，餘者改「。」）。
        （旧口徑按『相鄰非空行』併段，会把同一欄內各別成段之並列項連環搶佔『一枚』之額，
         致後者無端被改句號——第 66 輪改單位，教與第 57 輪『尺之單位錯則綠亦非綠』同。）
   理據：本書之說服力來自冷峻的陳述與偶發的一擊；同段連擊使二者俱失。
   用法：python -X utf8 _work/exchkr.py [--go]   （--go 則依則歸併，並印改處之數）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
GO = u"--go" in sys.argv
PAGES = 227                       # 無冊可開時之退路（末次重建 2026-10-27・第 78 輪兩式俱出 227 頁）
_GIVEN = any(a.startswith("--pages=") for a in sys.argv)
for a in sys.argv:
    if a.startswith('--pages='): PAGES = int(a[8:])
if not _GIVEN:                    # 分母自冊上取，不靠人手抄（形制一改，抄舊形之尺即假綠）
    import glob as _g
    _pdf = _g.glob(os.path.join(os.path.dirname(os.path.abspath(HP.SRC)),
                                "_print", u"佛陀的護欄_*影印版.pdf"))
    if _pdf:
        try:
            import pymupdf
            _d = pymupdf.open(_pdf[0])
            PAGES = _d.page_count
            _d.close()
            print(u"（頁數自冊算：%d・%s）" % (PAGES, os.path.basename(_pdf[0])[-8:]))
        except Exception as _e:                   # noqa: BLE001  冊壞則用退路之數，不擲不靜
            print(u"（頁數自冊算失敗，用退路 %d：%s）" % (PAGES, _e))
NL = chr(13) + chr(10)
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
starts = []
p = 0
for i, line in enumerate(L):
    starts.append(p)
    p += len(line)
    if i < len(L) - 1:
        p += len(NL)
assert p == len(raw), u"位移表與檔長不合"
spans = [(m.start(), m.end()) for m in re.finditer(u"「[^」]*」", raw)]


def inq(x):
    return any(a <= x < b for a, b in spans)


def narr(i, line):
    return [m.start() for m in re.finditer(u"！", line) if not inq(starts[i] + m.start())]


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hlpara                                                    # noqa: E402  印面段落之共器
APX = hlpara.apx_of(L)
blocks = [list(range(a, b)) for a, b in hlpara.blocks(L, APX)]
blocks += [[i] for i in range(APX)
           if L[i].strip() and hlpara.skip(L[i]) and not L[i].startswith(hlpara.FENCE)]
blocks.sort(key=lambda bl: bl[0])

tot = sum(len(narr(i, s)) for i, s in enumerate(L))
over = [(bl, sum(len(narr(i, L[i])) for i in bl)) for bl in blocks]
over = [(bl, c) for bl, c in over if c >= 2]
inqu = sum(len(narr(i, L[i])) for bl in blocks for i in bl)
print(u"印面段落 %d・管內嘆號 %d（全檔 %d）｜每頁 %.2f（以 %d 頁計）｜超出一枚之段 %d 段" % (
    len(blocks), inqu, tot, tot / PAGES, PAGES, len(over)))
for bl, c in over[:8]:
    print(u"   L%-5d ×%d｜%s" % (bl[0] + 1, c, L[bl[0]][:64]))
if not GO:
    print(u"（覆核模式，未寫檔；加 --go 即依『一段一嘆』歸併）")
    raise SystemExit(0)

cut = 0
for bl, c in over:
    seen = 0
    for i in bl:
        line = L[i]
        if not line:
            continue
        out = []
        base = starts[i]
        for j, ch in enumerate(line):
            if ch == u"！" and not inq(base + j):
                seen += 1
                if seen > 1:
                    ch = u"。"
                    cut += 1
            out.append(ch)
        L[i] = u"".join(out)
new = NL.join(L)
assert new.count(chr(13)) == new.count(chr(10)) == len(L) - 1, u"EOL 變形"
assert new.count(u"！"), u"嘆號全失"
if not cut:
    print(u"管內無超額段，未寫檔")
    raise SystemExit(0)
io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
print(u"已歸併 %d 枚（引號外嘆號 %d → %d）" % (cut, tot, tot - cut))
