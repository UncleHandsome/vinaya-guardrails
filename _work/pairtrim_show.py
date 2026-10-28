# -*- coding: utf-8 -*-
"""目視之招：試跑 pairtrim 之 plan()，自『第一階』起印一窗（長段新撰不可只報數）。"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
pt = importlib.import_module("pairtrim")

f = pt.F2
raw = (ROOT / f).read_bytes()
lines = raw.decode("utf-8").split("\r\n")
keep, rows, kept, exp, errs, notes = pt.plan(f, lines)
out = []
for k, l in enumerate(lines):
    if keep[k]:
        out.extend(l.split("\n"))
i = next(n for n, l in enumerate(out) if "第一階・前置管轄與界之閥" in l)
for n in range(i - 4, i + 44):
    print(f"{n:5d}|{out[n]}")
h = sum(1 for c in "\n".join(out[i:i + 40]) if "\u4e00" <= c <= "\u9fff")
print(f"\n窗內（40 行）漢字 {h:,}・護閘之誤：{errs}")
