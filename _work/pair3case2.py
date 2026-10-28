# -*- coding: utf-8 -*-
"""第八波・附問二・深：三案之本地卷段取證（走 _tk.read／_tk.norm，非自讀原文檔）。

口徑：折形只留漢字並依 _tk.FOLD 歸體，**另存『折形位➔原串位』之映射**，
      故命中處可回原串取窗（含標點者以原形出之，供目驗逐字）。
用法：python -X utf8 _work/pair3case2.py 關鍵詞 [關鍵詞…] [-w 窗] [-n 上限]
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk  # noqa: E402

FILES = sorted(glob.glob(os.path.join(_tk.ROOT, "原文", "*.txt")))
SEG, off = [], 0
for f in FILES:
    t = _tk.norm(_tk.read(f))
    SEG.append((os.path.basename(f), off, t))
    off += len(t) + 1
FULL = _tk.VINAYA

MAP, PLAIN = [], []
for i, c in enumerate(FULL):
    if "\u4e00" <= c <= "\u9fff":
        MAP.append(i)
        PLAIN.append(_tk.FOLD.get(c, c))
P = "".join(PLAIN)


def where(i):
    for name, st, t in SEG:
        if st <= i < st + len(t):
            return name
    return "?"


def show(key, w, lim):
    p = "".join(_tk.FOLD.get(c, c) for c in re.sub(r"[^\u4e00-\u9fff]", "", key))
    hits = [m.start() for m in re.finditer(re.escape(p), P)] if p else []
    print("── 「%s」%d 見" % (key, len(hits)))
    for h in hits[:lim]:
        o = MAP[h]
        print("     [%s] %s" % (where(o), re.sub(r"\s+", "", FULL[max(0, o - 14):o + w])[:168]))


args, skip = [], 0
for a in sys.argv[1:]:
    if skip:
        skip = 0
        continue
    if a in ("-w", "-n"):
        skip = 1
        continue
    if not a.startswith("-"):
        args.append(a)
W = int(sys.argv[sys.argv.index("-w") + 1]) if "-w" in sys.argv else 110
N = int(sys.argv[sys.argv.index("-n") + 1]) if "-n" in sys.argv else 10
for k in (args or ["阿梨吒", "捕鷲", "偷羅難陀", "溫室", "畢陵伽婆蹉", "婢", "恒水神"]):
    show(k, W, N)
