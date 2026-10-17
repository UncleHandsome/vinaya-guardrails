# -*- coding: utf-8 -*-
"""第 99 輪套改：附錄指針之空形統一（『附錄 E』→『附錄E』）；附錄L 之欄目乃 `_tk.py` 取數之鍵，不預。"""
import io, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
aL = next(i for i, l in enumerate(L) if l.startswith("# 附錄L"))
bL = next(i for i, l in enumerate(L) if i > aL and l.startswith("# "))
c = collections.Counter()
for i, l in enumerate(L):
    if aL <= i < bL:
        continue
    n = re.sub(r"附錄[ \u3000]+([A-M])(?![A-Za-z0-9])", r"附錄\1", l)
    if n != l:
        for m in re.finditer(r"附錄([A-M])", l):
            pass
        c[i] = len(re.findall(r"附錄[ \u3000]+[A-M]", l))
        L[i] = n
io.open(MD, "w", encoding="utf-8").write("\n".join(L))
print("改動行 %d｜指針 %d 處" % (len(c), sum(c.values())))
print("附錄L 內仍存空形（鍵也）：%d 處" % len(re.findall(r"附錄[ \u3000]+[A-M]", "\n".join(L[aL:bL]))))
