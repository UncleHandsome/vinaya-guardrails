# -*- coding: utf-8 -*-
"""刀後重災行：於『已落盤』之正本直查世俗法字眼，印出當前行號與上下文，供手改之第七刀。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib
m = importlib.import_module("pairdelaw")
P = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"

RX = m.HAS_LAW          # 只認『實定法之名與機制』；本書自制之『法定・法律』不在其內
lines = P.read_bytes().decode("utf-8").split("\r\n")
fence = m.fence_mask(lines)
rows = []
for i, l in enumerate(lines, 1):
    hits = RX.findall(l)
    if hits:
        rows.append((i, len(hits), "".join(sorted(set(hits))), l.strip()[:100], fence[i - 1]))
print(f"重災行 {len(rows)} 行・命中 {sum(r[1] for r in rows)} 見"
      f"（圍欄內 {sum(r[1] for r in rows if r[4])} 見・其圖表另刀）\n")
for i, h, k, t, f in rows:
    if not f:
        print(f"L{i} ({h}) [{k}] {t}")
