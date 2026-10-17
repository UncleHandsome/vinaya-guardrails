# -*- coding: utf-8 -*-
"""第 100 輪探針六：節號重號與跳號（逐章列出實有節號）。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
CN = {c: i for i, c in enumerate("零一二三四五六七八九", 0)}


def c2n(s):
    m = re.fullmatch(r"([一二三四五六七八九])?十([一二三四五六七八九])?", s)
    if m:
        return CN.get(m.group(1), 1) * 10 + CN.get(m.group(2), 0)
    return CN.get(s)


blocks = [i for i, l in enumerate(L) if re.match(r"^# (第[一二三四五六七八九]章|附錄[A-M]|結語|終卷)", l)]
blocks.append(len(L))
for b in range(len(blocks) - 1):
    a, z = blocks[b], blocks[b + 1]
    title = L[a].lstrip("# ")[:12]
    raw = []
    for i in range(a + 1, z):
        if L[i].startswith("### "):
            m = re.match(r"^第([一二三四五六七八九十]+)節", L[i][4:])
            if m:
                raw.append((i + 1, c2n(m.group(1))))
    ns = [n for _, n in raw]
    if not ns:
        continue
    dup = sorted({n for n in ns if ns.count(n) > 1})
    gap = [n for n in range(min(ns), max(ns) + 1) if n not in ns]
    flag = "　← 重號%s" % dup if dup else ""
    flag += "　← 跳號%s" % gap if gap else ""
    print("%-14s 節號 %s%s" % (title, ns, flag))
