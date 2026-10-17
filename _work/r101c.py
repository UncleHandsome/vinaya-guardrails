# -*- coding: utf-8 -*-
"""第 101 輪探針三：表格完整性——欄數一致、分隔列俱在、無孤行。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")


def cells(l):
    return [c.strip() for c in l.strip().strip("|").split("|")]


def head_of(i):
    for j in range(i, -1, -1):
        if L[j].startswith("# "):
            return L[j].lstrip("# ")[:14]
    return "卷首"


i = 0
n = rag = nosep = 0
while i < len(L):
    if L[i].lstrip().startswith("|"):
        j = i
        rows = []
        while j < len(L) and L[j].lstrip().startswith("|"):
            rows.append(j)
            j += 1
        n += 1
        w = [len(cells(L[k])) for k in rows]
        base = max(set(w), key=w.count)
        odd = [(rows[t] + 1, w[t]) for t in range(len(rows)) if w[t] != base]
        if len(rows) > 1 and not re.fullmatch(r"[|:\-\s]+", L[rows[1]]):
            nosep += 1
            print("  缺分隔列 %-12s L%d｜%s" % (head_of(rows[0]), rows[0] + 1, L[rows[0]][:40]))
        if odd:
            rag += 1
            print("  欄數不齊 %-12s 表首 L%d 應 %d 欄，異者 %s" % (
                head_of(rows[0]), rows[0] + 1, base, odd[:6]))
        i = j
    else:
        i += 1
print("表 %d 張｜欄數不齊 %d 張｜缺分隔列 %d 張" % (n, rag, nosep))
