# -*- coding: utf-8 -*-
"""第 96 輪探針二：反引號與工程縮語之落點歸屬。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")

def head_of(i):
    for j in range(i, -1, -1):
        if L[j].startswith("# "):
            return L[j][:34]
    return "卷首"

tick = collections.Counter(); fail = collections.Counter()
for i, l in enumerate(L):
    if l.startswith("# 附錄C") or l.startswith("# 附錄K") or l.startswith("# 附錄L") or l.startswith("# 附錄M"):
        pass
    n = len(re.findall(r"`[^`\n]{1,40}`", l))
    if n:
        tick[head_of(i)] += n
    m = len(re.findall(r"\bFAIL\b|\bPASS\b|\bSOP\b", l))
    if m:
        fail[head_of(i)] += m
print("== 反引號 按大節 ==")
for k, v in tick.most_common(30):
    print("  %4d  %s" % (v, k))
print("== FAIL/PASS/SOP 按大節 ==")
for k, v in fail.most_common(30):
    print("  %4d  %s" % (v, k))
