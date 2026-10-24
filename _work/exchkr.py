# -*- coding: utf-8 -*-
"""嘆號密度尺（exchkr）：只量「引號外」之感嘆號——引號內多為律文原話（「咄！男子！」之類），不較。
   口徑：以空行分隔為一段；一段之內引號外之「！」至多一枚（首見留，餘者改「。」）。
   理據：本書之說服力來自冷峻的陳述與偶發的一擊；同段連擊使二者俱失。
   用法：python -X utf8 _work/exchkr.py [--go]   （--go 則依則歸併，並印改處之數）
"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
GO = u"--go" in sys.argv
PAGES = 288                       # 末次重建（2026-10-19）288 頁；重建後須隨動，或給 --pages=N
for a in sys.argv:
    if a.startswith('--pages='): PAGES = int(a[8:])
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


blocks, cur = [], []
for i, s in enumerate(L):
    if s.strip() == u"":
        if cur:
            blocks.append(cur)
        cur = []
    else:
        cur.append(i)
if cur:
    blocks.append(cur)

tot = sum(len(narr(i, s)) for i, s in enumerate(L))
over = [(bl, sum(len(narr(i, L[i])) for i in bl)) for bl in blocks]
over = [(bl, c) for bl, c in over if c >= 2]
print(u"引號外嘆號 %d 枚｜每頁 %.2f（以 %d 頁計）｜超出一枚之段 %d 段" % (tot, tot / PAGES, PAGES, len(over)))
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
assert new.count(u"！") and cut, u"無可歸併者"
io.open(BOOK, "w", encoding="utf-8", newline="").write(new)
print(u"已歸併 %d 枚（引號外嘆號 %d → %d）" % (cut, tot, tot - cut))
