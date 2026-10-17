# -*- coding: utf-8 -*-
"""第 96 輪探針九：印面跨章克隆句（純漢字 16 字滑窗，相連窗自動合併）。"""
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
            return L[j].replace("# ", "")[:8]
    return "卷首"
seen = collections.defaultdict(list)
for i, l in enumerate(L):
    if i in skip or not l.strip():
        continue
    t = re.sub(r"[*`>|\s#-]+", "", l)
    for k in range(0, max(0, len(t) - 15)):
        w = t[k:k + 16]
        if re.fullmatch(r"[一-鿿]{16}", w):
            seen[w].append(i + 1)
dup = sorted([(w, sorted(set(v))) for w, v in seen.items() if len(set(v)) > 1],
             key=lambda x: x[1][0])
out = []
for w, ls in dup:
    if out and w[:15] == out[-1][0][-15:]:
        out[-1] = [out[-1][0] + w[-1], sorted(set(out[-1][1] + ls))]
        continue
    out.append([w, ls])
for w, ls in out:
    if len(w) < 16:
        continue
    print("%2d 處｜%s｜L%s｜%s" % (len(ls), "·".join(head_of(x - 1) for x in ls[:5]),
                                 ",".join(map(str, ls[:8])), w[:70]))
print("合併後 %d 組" % len(out))
