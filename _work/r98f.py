# -*- coding: utf-8 -*-
"""第 96 輪探針六：markdown 殘相與句讀硬傷。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
skip = set(); fence = []
for i, l in enumerate(L):
    if l.startswith(("# 附錄C", "# 附錄K", "# 附錄L", "# 附錄M")):
        j = i + 1
        while j < len(L) and not L[j].startswith("# "):
            j += 1
        skip.update(range(i, j))
def head_of(i):
    for j in range(i, -1, -1):
        if L[j].startswith("# "):
            return L[j][:22]
    return "卷首"
inb = False; n = 0
for i, l in enumerate(L):
    if i in skip or not l.strip():
        continue
    if l.startswith("```"):
        inb = not inb; continue
    if inb:
        continue
    h = []
    if l.count("**") % 2:
        h.append("粗體不成對")
    if re.search(r"[，、：；]\s*[。，]", l):
        h.append("疊點")
    if re.search(r"（）|\(\)", l):
        h.append("空括弧")
    if re.search(r"。{2,}|，{2,}", l):
        h.append("重複標點")
    if re.search(r"：\s*$", l.rstrip()) and l.rstrip().endswith("：") and i + 1 < len(L) and not L[i+1].strip():
        h.append("冒號收尾接空行")
    if re.search(r"TODO|待定|待補|暫缺|XXX|（略）|\.\.\.|……\Z", l):
        h.append("佔位/存目")
    if "  " in re.sub(r"^#+ ", "", l) and not l.startswith("|") and "  " in l.rstrip()[-4:] and l.endswith("  "):
        pass
    if h:
        n += 1
        print("L%-6d %-20s %-14s %s" % (i + 1, head_of(i), "＋".join(h), l[:80]))
print("計 %d" % n)
