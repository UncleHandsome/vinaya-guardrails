# -*- coding: utf-8 -*-
"""第 101 輪探針二：卷首目錄逐條對勘實有標題（含次級條目）。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
a = next(i for i, l in enumerate(L) if l.startswith("## 【全書開卷標準目錄】"))
b = next(i for i, l in enumerate(L) if i > a and l.startswith("# 第一章"))


def norm(t):
    t = re.split(r"[（(]", t)[0]
    t = t.replace("**", "").replace("【", "").replace("】", "")
    return re.sub(r"[　 :：、，\-—]", "", t).strip()


heads = {}
for i, l in enumerate(L):
    m = re.match(r"^#{1,5}\s+(.*)$", l)
    if m:
        heads.setdefault(norm(m.group(1)), i + 1)
exact = fuzzy = miss = 0

bad = []
for i in range(a, b):
    l = L[i]
    m = re.match(r"^\s*\*\s+(.+)$", l)
    if not m:
        continue
    t = norm(m.group(1))
    if not t:
        continue
    if t in ("附錄", "目錄"):
        continue
    if t in heads:
        exact += 1
        continue
    hit = [k for k in heads if k.startswith(t) or t.startswith(k)]
    if hit:
        fuzzy += 1
        bad.append((i + 1, "近似", m.group(1).strip()[:44], " ↔ ".join(sorted(hit)[:2])[:60]))
    else:
        miss += 1
        bad.append((i + 1, "無著", m.group(1).strip()[:44], ""))
print("目錄條目：全合 %d、近似 %d、無著 %d" % (exact, fuzzy, miss))
for ln, k, t, h in bad:
    print("  L%-6d %s ｜%s｜%s" % (ln, k, t, h))

print("全合 %d、近似 %d、無著 %d" % (exact, fuzzy, miss))
