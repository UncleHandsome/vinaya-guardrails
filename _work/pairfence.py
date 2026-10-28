# -*- coding: utf-8 -*-
"""圍欄回量之未入稽核者，逐段點名（量產物：源 md 段 ↔ FINAL html 之 <pre>）。

用法：python -X utf8 _work/pairfence.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_print"))
sys.path.insert(0, str(ROOT))
sys.argv = ["build38", "full", "screen"]
import build_hulan as bh        # noqa: E402
import pymupdf as pm            # noqa: E402

for key, name in (("1", "起心動念"), ("2", "如法推尋")):
    md = ROOT / "_print" / ("pair_%s_screen.md" % key)
    fin = ROOT / "_print" / ("final_pair%s_screen.html" % key)
    pdf = ROOT / "_print" / ("pair%s_screen.pdf" % key)
    if not (md.is_file() and fin.is_file()):
        print("跳過 %s（中介檔不在）" % name)
        continue
    lines = io.open(md, encoding="utf-8").read().split("\n")
    blocks = bh.fence_blocks(lines)
    bh.FINAL = str(fin)
    bh.FENCE_BLOCKS = blocks
    mp, ntag, miss = bh.pre_tag_map(blocks)
    print("=" * 70)
    print("■ %s｜源圍欄 %d 段・印面 <pre> %d 個・配對 %d・配對失敗 %s"
          % (name, len(blocks), ntag, len(mp), miss or "無"))
    if pdf.is_file():
        d = pm.open(str(pdf))
        au = bh.pre_audit(d, blocks, bh.pre_base_sizes(), mp)
        d.close()
        un = sorted(set(range(1, len(blocks) + 1)) - set(au))
        print("  入稽核 %d/%d 段・未入 %s" % (len(au), len(blocks), un or "無"))
        for k in un:
            b = blocks[k - 1]
            print("    #%d 未入｜源首行「%s」｜行數 %d｜末行「%s」"
                  % (k, (b[0][:52] if b else ""), len(b), (b[-1][:40] if b else "")))
            if k in mp:
                print("       已配到標籤 #%d（故非配對失敗，乃 pre_audit 判序未覆）" % mp[k])
        thin = [(k, v) for k, v in sorted(au.items()) if isinstance(v, dict) and v.get("size", 99) < 9]
        if thin:
            print("  9pt 以下之段：%s" % thin)
