# -*- coding: utf-8 -*-
"""案卡之點名：刀前刀後逐卡列名，驗『15 − 14』之差確是壬刀之跨冊指針帶字，非多出一卡。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"
B = ROOT / "_archive/備份/AI清理前/如法推尋：僧伽憲政、法權審理與修復正義.txt.pre_delaw"
CARD = re.compile(r"【現代演繹判例|【制度案卷|【案卷\s")

for tag, p in (("刀前", B), ("刀後", P)):
    lines = p.read_bytes().decode("utf-8").split("\r\n")
    print("■", tag)
    for i, l in enumerate(lines, 1):
        for x in CARD.findall(l):
            print("   L%-5d %-14s %s" % (i, x, l.strip()[:60]))
