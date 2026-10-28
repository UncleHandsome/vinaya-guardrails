# -*- coding: utf-8 -*-
"""第三波・逐條落點：外來語括號與現代譯名之每一處原文（供改寫之對照，不摘要）。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")

W = sys.argv[1] if len(sys.argv) > 1 else None
RX = re.compile(W)
for tag, ls in (("F2", F2), ("F1", F1)):
    inf = m.fence_mask(ls)
    print("=" * 76)
    print("■", tag)
    for i, l in enumerate(ls, 1):
        if RX.search(l):
            print("  L%-5d%s %s" % (i, "欄" if inf[i - 1] else "　", l.strip()[:118]))
