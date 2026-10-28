# -*- coding: utf-8 -*-
"""欄寬漂移之檢：第三波諸刀（子・丑・寅・卯）換字前後，圍欄內之行寬須不動；動者點名。"""
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = "```"
PAIRS = [("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt",
          "_archive/備份/AI清理前/如法推尋：僧伽憲政、法權審理與修復正義.txt.pre_purge"),
         ("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
          "_archive/備份/AI清理前/起心動念：四分律的心智顯微鏡與唯識解剖.txt.pre_purge")]


def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def fences(ls):
    out, inside, start = {}, False, 0
    for i, l in enumerate(ls):
        if l.strip().startswith(FENCE):
            if not inside:
                inside, start = True, i
            else:
                inside = False
            continue
        if inside:
            out[i] = l
    return out


def in_fence_flags(ls):
    out, inside = [], False
    for l in ls:
        if l.strip().startswith(FENCE):
            out.append(inside)
            inside = not inside
        else:
            out.append(inside)
    return out


for tag, cur, bak in PAIRS:
    a = (ROOT / bak).read_bytes().decode("utf-8").split("\r\n")
    b = (ROOT / cur).read_bytes().decode("utf-8").split("\r\n")
    fa, fb = in_fence_flags(a), in_fence_flags(b)
    import difflib
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    drift = []
    for tag_, t1, t2, u1, u2 in sm.get_opcodes():
        if tag_ != "replace" or (t2 - t1) != 1 or (u2 - u1) != 1 or a[t1] == b[u1]:
            continue
        i = u1
        if not (fa[t1] and fb[i]):
            continue
        if dw(a[t1]) != dw(b[i]):
            drift.append((i + 1, dw(a[t1]), dw(b[i]), a[t1].strip()[:40], b[i].strip()[:40]))
    print(f"■ {tag}・行 {len(a)} → {len(b)}・圍欄內寬度漂移 {len(drift)} 行（同位對齊後）")
    for i, w1, w2, o, n in drift[:16]:
        print(f"    L{i:<6} {w1}→{w2}\n      故 {o}\n      新 {n}")
