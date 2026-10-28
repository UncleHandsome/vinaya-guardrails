# -*- coding: utf-8 -*-
"""記憶檔之簡形歸正（逐枚目驗，非前綴通配）：本檔只改 project-pair-books-delaw.md。"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Users\lionc\OneDrive\桌面\教務交接\星韋師\戒律分析") / "_work"))
import importlib
sm = importlib.import_module("_simpmap")
sd = importlib.import_module("_simpdict")
S = (set(sm.MAP) | set(sd.MAP)) - set("几")

P = Path(r"C:\Users\lionc\.qoder\projects\C--Users-lionc-OneDrive-----------------\memory\project-pair-books-delaw.md")
FIX = [("当代", "當代"), ("本轮", "本輪"), ("边际", "邊際"), ("否则", "否則"), ("页眉", "頁眉")]
raw = io.open(P, encoding="utf-8").read()
for o, n in FIX:
    c = raw.count(o)
    print("換 %s → %s・命中 %d" % (o, n, c))
    raw = raw.replace(o, n)
io.open(P, "w", encoding="utf-8", newline="").write(raw)
bad = [(i, "".join(sorted(set(c for c in l if c in S)))) for i, l in enumerate(raw.split("\n"), 1)
       if any(c in S for c in l)]
print("歸正後簡形行：", bad)
