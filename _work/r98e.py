# -*- coding: utf-8 -*-
"""第 96 輪探針五：標點、括號、疊字之硬傷普查。"""
import io, os, re

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
            return L[j][:24]
    return "卷首"
n = 0
for i, l in enumerate(L):
    if i in skip or not l.strip() or l.startswith("|"):
        continue
    t = re.sub(r"`[^`]*`", "", l)
    hits = []
    if t.count("（") != t.count("）"):
        hits.append("括弧不成對 %d/%d" % (t.count("（"), t.count("）")))
    if t.count("【") != t.count("】"):
        hits.append("方括不成對")
    if t.count("『") != t.count("』"):
        hits.append("單引不成對")
    if re.search(r"[一-鿿],|,[一-鿿]", t):
        hits.append("半形逗號")
    if re.search(r"[一-鿿]\.(?!\d)|\.[一-鿿]", t):
        hits.append("半形句點")
    if re.search(r"[一-鿿];|;[一-鿿]", t):
        hits.append("半形分號")
    if re.search(r"[一-鿿]\((?!\d)|\)[一-鿿]", t):
        hits.append("半形圓括")
    m = re.search(r"([\u4e00-\u9fff])\1\1", t)
    if m:
        hits.append("三字疊 %s" % m.group(1))
    if re.search(r" 　|　 {2}", t):
        hits.append("空白混全形")
    if hits:
        n += 1
        print("L%-6d %-22s %s ｜%s" % (i + 1, head_of(i), "＋".join(hits), l[:90]))
print("計 %d 行" % n)
