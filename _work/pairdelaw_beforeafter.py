# -*- coding: utf-8 -*-
"""刀前／刀後之形制對照：章數・章末呼吸口・判例卡・圍欄段・法名。一輪之損益須兩面同印。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUR = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"
OLD = ROOT / "_archive/備份/AI清理前/如法推尋：僧伽憲政、法權審理與修復正義.txt.pre_delaw"
F1 = ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
F1OLD = ROOT / "_archive/備份/AI清理前/起心動念：四分律的心智顯微鏡與唯識解剖.txt.pre_delaw3"

RE_CH = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+章[　 ]")
RE_BR = re.compile(r"^#{1,6}\s*【本章章末")
RE_JIE = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]")
CARD = re.compile(r"【現代演繹判例|【制度案卷|【案卷\s")


def stat(lines, tag):
    import sys
    sys.path.insert(0, str(ROOT / "_work"))
    import importlib
    m = importlib.import_module("pairdelaw")
    han = sum(1 for c in "\n".join(lines) if "\u4e00" <= c <= "\u9fff")
    print("  %-6s 行 %5d・漢字 %6s・章 %2d・節 %3d・呼吸口 %2d・案卡 %2d・圍欄段 %3d・法名 %3d"
          % (tag, len(lines), format(han, ","), len([l for l in lines if RE_CH.match(l.strip())]),
             len([l for l in lines if RE_JIE.match(l.strip())]),
             len([l for l in lines if RE_BR.match(l.strip())]),
             len([x for l in lines for x in CARD.findall(l)]),
             len([x for x, f in zip(lines, m.fence_mask(lines)) if x.strip().startswith("```") and not f]) // 2,
             sum(len(m.HAS_LAW.findall(l)) for l in lines)))


def rd(p):
    return p.read_bytes().decode("utf-8").split("\r\n")


print("■ 法制卷（如法推尋）")
stat(rd(OLD), "刀前")
stat(rd(CUR), "刀後")
print("■ 心法卷（起心動念）")
stat(rd(F1OLD), "刀前")
stat(rd(F1), "刀後")
