# -*- coding: utf-8 -*-
"""只重做合冊（不重畫兩冊）：取現成之兩卷 PDF，走 build_pair.merge() 同一法源接排。
用法：python -X utf8 _work/pairmerge_only.py screen|print"""
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "_print"
mode = (sys.argv[1] if len(sys.argv) > 1 else "screen").lower()
sys.argv = ["build_pair", mode]
sys.path.insert(0, str(HERE))
import build_pair as bp  # noqa: E402  （匯入時即按 argv 定 TAG）

TAG = bp.TAG
parts = [str(HERE / ("pair1%s.pdf" % TAG)), str(HERE / ("pair2%s.pdf" % TAG))]
for p in parts:
    if not os.path.isfile(p):
        raise SystemExit("缺卷檔：%s（須先出該式之兩冊）" % p)
# 交付檔名（雨冊之名帶書名，_pair*.pdf 為其中間檔・同頁同籤）——名一律取自 build_pair，不二抄
delivered = [str(HERE / (cfg["out"] + bp.TAGL + ".pdf")) for cfg in bp.BOOKS]
for p in delivered:
    if os.path.isfile(p):
        parts = delivered
        break
meta = {"title": "雙子星合冊｜起心動念（心法卷）＋如法推尋（法制卷）｜%s" % bp.TAGL,
        "author": "編者", "subject": "四分律之心智現象學與僧伽憲政學",
        "keywords": "四分律；毘奈耶；心所；羯磨；大正藏 No.1428",
        "creator": "build_pair 管線（沿用 build38 之法源）", "producer": "build_pair",
        "_out": bp.merged_name(bp.TAGL)}
print("接排：%s" % " ＋ ".join(os.path.basename(x)[:12] for x in parts))
out, n, t = bp.merge(parts, meta)
print("✓ %s｜%d 頁・書籤接排 %d 條" % (os.path.basename(out), n, t))
