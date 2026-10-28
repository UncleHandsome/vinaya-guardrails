# -*- coding: utf-8 -*-
"""刀五之候選點名：卷首四禁之語，逐章重複者方是冗；嵌在制度內之規則（反坐、與狂癡羯磨）非冗。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")

F2 = (ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt").read_bytes().decode("utf-8").split("\r\n")
F1 = (ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt").read_bytes().decode("utf-8").split("\r\n")
ECHO = (r"向外照人|刺探|道德審判|心理誅心|獵巫|日用臥榻|長眠臥榻|急診室當|病房認作|"
        r"良知過載|神經質|強迫症|以清淨自高|居高臨下|抓到把柄|施虐|酷吏|拿本書|"
        r"不是.{0,4}凶器|非用以傷人|當成長眠")

for tag, lines in (("F1 心法卷", F1), ("F2 法制卷", F2)):
    print("=" * 74)
    print("■", tag)
    cur = ""
    for i, l in enumerate(lines):
        mm = re.match(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+章[　 ][^\n]{0,14})", l.strip())
        if mm:
            cur = mm.group(1)
        if re.search(ECHO, l):
            print(f"  {cur[:16]:18s} L{i + 1}|{l.strip()[:70]}")
