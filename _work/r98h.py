# -*- coding: utf-8 -*-
"""第 96 輪探針八：印面跨章克隆句（15 字滑窗）。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
skip = set()
for i, l in enumerate(L):
    if l.startswith(("# 附錄C", "# 附錄K", "# 附錄L", "# 附錄M")):
        j = i + 1
        while j < len(L) and not L[j].startswith("# "):
            j += 1
        skip.update(range(i, j))
def head_of(i):
    for j in range(i, -1, -1):
        if L[j].startswith("# "):
            return L[j][:20]
    return "卷首"
seen = collections.defaultdict(list)
for i, l in enumerate(L):
    if i in skip or not l.strip():
        continue
    t = re.sub(r"[*`>|\s#-]+", "", l)
    for k in range(0, max(0, len(t) - 15)):
        w = t[k:k + 15]
        if re.search(r"[，。；：、（）【】]", w):
            continue
        seen[w].append(i + 1)
dup = [(w, ls) for w, ls in seen.items() if len(set(ls)) > 1]
# 聚為較長片段
merged = []
for w, ls in sorted(dup, key=lambda x: -len(set(x[1]))):
    if any(w in m[0] for m in merged[:60]):
        continue
    merged.append((w, sorted(set(ls))))
for w, ls in merged[:45]:
    print("%3d 處  L%-6s …%-6s ｜ %s" % (len(ls), ls[0], ls[-1], w))
print("克隆窗數 %d，去重後列 %d" % (len(dup), len(merged)))
