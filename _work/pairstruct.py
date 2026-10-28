# -*- coding: utf-8 -*-
"""第八波・附問一：心法卷章↔案之戶口（奉『每章至少三案』之新令，先量再排）。

用法：python -X utf8 _work/pairstruct.py [檔名…]   （缺＝兩冊俱量）
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HAN = "〇一二三四五六七八九十百"
RE_PIAN = re.compile(r"^#{1,6}\s*(第[%s]+篇[:：][^\n]*)$" % HAN)
RE_ZHANG = re.compile(r"^#{1,6}\s*(第[%s]+章[　 ][^\n]*)$" % HAN)
RE_JIE = re.compile(r"^#{1,6}\s*(第[%s]+節[　 ][^\n]*)$" % HAN)
RE_APX = re.compile(r"^#{1,6}\s*(附錄[一二三四][　 ][^\n]*)$")
RE_CARD = re.compile(r"[【\[](?:制度)?案卷\s*([0-9]{2,3}[A-Z]?)")
CN = {c: i for i, c in enumerate("一二三四五六七八九十百", 1)}


def cn2int(s):
    s = s.split("：")[0]
    m = re.match(r"第([%s]+)[篇章節]" % HAN, s)
    t, out = m.group(1), 0
    if t == "十":
        return 10
    while t:
        if t[0] == "十":
            out += 10 * (CN.get(t[1], 1) if len(t) > 1 else 1)
            t = t[2:] if len(t) > 1 else ""
        else:
            if len(t) > 1 and t[1] == "十":
                out += CN[t[0]] * 10
                t = t[2:]
            else:
                out += CN[t[0]]
                t = t[1:]
    return out


def census(path):
    lines = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n")
    fence, f = [], False
    for l in lines:
        if re.match(r"^\s*```", l):
            f = not f
        fence.append(f)
    cur_p, cur_c = None, None
    book = []
    for i, l in enumerate(lines, 1):
        if fence[i - 1]:
            continue
        s = l.strip()
        m = RE_PIAN.match(s) or RE_APX.match(s)
        if m:
            if m is RE_PIAN.match(s):
                cur_p = m.group(1)
            else:
                cur_p = m.group(1)[:12]
            cur_c = None
            continue
        if RE_ZHANG.match(s):
            cur_c = {"z": RE_ZHANG.match(s).group(1), "ln": i, "jie": 0, "cards": []}
            book.append((cur_p, cur_c))
            continue
        if RE_JIE.match(s) and cur_c:
            cur_c["jie"] += 1
        mc = RE_CARD.search(s)
        if mc and cur_c and (s.startswith("#") or s.startswith("**【") or s.startswith("【案卷")):
            cur_c["cards"].append(mc.group(1))
    return book


for name in (sys.argv[1:] or ["起心動念：四分律的心智顯微鏡與唯識解剖.txt",
                              "如法推尋：僧伽憲政、法權審理與修復正義.txt"]):
    p = Path(ROOT) / name
    bk = census(p)
    print("=" * 76)
    print("■", name[:12], "・章 %d" % len(bk))
    bad = 0
    for pian, c in bk:
        n = len(c["cards"])
        flagx = "  ← 未足三案" if n < 3 else ""
        if n < 3:
            bad += 1
        print("  %-8s %-34s L%-5d 節 %2d・案 %2d %s%s"
              % ((pian or "")[:8], c["z"][:34], c["ln"], c["jie"], n, "、".join(c["cards"]), flagx))
    print("  未足三案之章：%d／%d" % (bad, len(bk)))
