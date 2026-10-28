# -*- coding: utf-8 -*-
"""指針之檢：『第三章閘門四』『第六章〔案例 21〕』之类之跨段指針，於三冊（F1/F2/ver39）中查其落點。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ["如法推尋：僧伽憲政、法權審理與修復正義.txt",
           "起心動念：四分律的心智顯微鏡與唯識解剖.txt",
           "ver39四分律_起心動念心智分析框架_修正版.md"]
PAT = re.compile(r"閘門[〇一二三四五六七八九十0-9]+|案例\s*21|案卷\s*21")

for fn in TARGETS:
    p = ROOT / fn
    if not p.exists():
        print("（無此檔）", fn)
        continue
    lines = p.read_bytes().decode("utf-8", "replace").replace("\r\n", "\n").split("\n")
    hits = [(i, l.strip()[:70]) for i, l in enumerate(lines, 1) if PAT.search(l)]
    heads = [(i, l.strip()[:60]) for i, l in enumerate(lines, 1)
             if re.match(r"^#{1,6}\s", l.strip()) and re.search(r"閘門|案卷 21|案例 21", l)]
    print("=" * 70)
    print("■", fn, "・命中", len(hits), "行")
    for i, t in hits:
        print(f"   L{i}|{t}")
    print("   含『閘門/21』之標題：", heads)
