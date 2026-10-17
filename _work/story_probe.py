# -*- coding: utf-8 -*-
"""因緣探針：在《四分律》六檔語料中找關鍵字，報檔案・最近之篇題（行首無空格者）・前後文。
用法：python -X utf8 _work/story_probe.py 詞1 詞2 …（多詞＝同一段須俱含，先各詞單查再合查由人判）
     加 --near 詞A 詞B → 只報兩詞相距 ≤N 字之段（N 預設 260）
"""
import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES = sorted(glob.glob(os.path.join(ROOT, "原文", "*.txt")))
CORPUS = []
for f in FILES:
    s = io.open(f, encoding="utf-8").read().replace("\r\n", "\n")
    CORPUS.append((os.path.basename(f), s))


def heads(name, s, pos):
    """回傳該位置之前最近之『篇／卷題』（行首不為空格者）。"""
    out = ""
    for m in re.finditer(u"(?m)^[^ 　\\n]{2,28}$", s[:pos]):
        t = m.group(0).strip()
        if re.search(u"(卷第|法之?[一二三四五六七八九十]|犍度|法$)", t):
            out = t
    return out


def show(name, s, i, span=90):
    print(u"  【%s｜%s｜@%d】…%s…" % (name[:5], heads(name, s, i), i,
          s[max(0, i - 18):i + span].replace("\n", "/")))


mode = "each"
args = sys.argv[1:]
if args and args[0] == "--near":
    mode = "near"
    args = args[1:]

if mode == "each":
    for kw in args:
        n = 0
        print("=== 詞：%s" % kw)
        for name, s in CORPUS:
            for m in re.finditer(re.escape(kw), s):
                show(name, s, m.start())
                n += 1
                if n >= 4:
                    break
            if n >= 4:
                break
        if not n:
            print("  （語料無此詞）")
else:
    a, b = args[0], args[1]
    N = int(args[2]) if len(args) > 2 else 260
    tot = 0
    print("=== 並現：%s ＋ %s（相距 ≤%d 字）" % (a, b, N))
    for name, s in CORPUS:
        for m in re.finditer(re.escape(a), s):
            for k in re.finditer(re.escape(b), s[max(0, m.start() - N):m.start() + N]):
                show(name, s, m.start(), 200)
                tot += 1
                break
            if tot >= 6:
                break
        if tot >= 6:
            break
    if not tot:
        print("  （無並現之段）")
