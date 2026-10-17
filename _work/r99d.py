# -*- coding: utf-8 -*-
"""第 97 輪探針：標題自身重述（X：…X…）與首尾同語。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
L = io.open(MD, encoding="utf-8").read().split("\n")
n = 0
for i, l in enumerate(L):
    if not re.match(r"^#{2,5} ", l):
        continue
    t = l.lstrip("#").strip()
    parts = re.split(r"[：:（(]", t)
    seen = set()
    for p in parts:
        for k in range(len(p) - 3):
            g = p[k:k + 4]
            if re.fullmatch(r"[一-鿿]{4}", g) and g in seen:
                n += 1
                print("L%-6d %s" % (i + 1, t[:76]))
                break
        else:
            seen.update({p[k:k + 4] for k in range(len(p) - 3)
                         if re.fullmatch(r"[一-鿿]{4}", p[k:k + 4])})
print("計 %d 條標題自我重述" % n)
