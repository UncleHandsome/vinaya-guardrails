# -*- coding: utf-8 -*-
"""兩輪之形制對照：一輪後（基線）vs 今正本。宣稱須與實測同印，基線須自證同齡。

基線之 tag 不可亂挑：`.pre_delaw4`／`.pre_purge` 已被歷次重跑覆寫（今存 5,275／4,651 行＝雙附錄之敗筆），
唯 `.pre_trim` 未再觸及，仍是一輪後之真身（帳上 F2 4,553・F1 3,246）。行數與帳不合者，本器明言『勿據此對照』。
"""
import hashlib
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
m = importlib.import_module("pairdelaw")

FENCE = "```"
CH = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+章[　 ]")
JIE = re.compile(r"^#{1,6}\s*第[〇一二三四五六七八九十]+節[　 ]")
BREATH = re.compile(r"^#{1,6}\s*(第[〇一二三四五六七八九十]+節[　 ]章末指針|【本章章末|【林下留白)")
# 案卡與提撕之形，兩冊本異（心法卷【案卷 NN】・法制卷【制度案卷 NN】；提撕作「【第N章提撕：…】」）——
# 舊口徑只認法制卷之形，故心法卷長年報「案卡 1・提撕 0」之殭數（尺覆 0 段仍似綠，與所量者異其域）。
CARD = re.compile(r"^#{1,6}\s*[【\[](?:制度)?案卷\s*[0-9]{2}")
TI = re.compile(r"【第[〇一二三四五六七八九十]+章提撕")

PAIRS = [("F2 法制卷", "如法推尋：僧伽憲政、法權審理與修復正義.txt"),
         ("F1 心法卷", "起心動念：四分律的心智顯微鏡與唯識解剖.txt")]
BASETAG = "pre_trim"
EXPECT = {"如法推尋：僧伽憲政、法權審理與修復正義.txt": 4553,
          "起心動念：四分律的心智顯微鏡與唯識解剖.txt": 3246}


def stat(ls, tag):
    h = sum(1 for c in "\n".join(ls) if "\u4e00" <= c <= "\u9fff")
    fences = len([1 for x, f in zip(ls, m.fence_mask(ls)) if x.strip().startswith(FENCE) and not f]) // 2
    print("  %-8s 行 %5d・漢字 %6s・章 %2d・節 %3d・呼吸 %2d・提撕 %2d・案卡 %2d・圍欄 %3d・法名 %3d"
          % (tag, len(ls), format(h, ","), len([l for l in ls if CH.match(l.strip())]),
             len([l for l in ls if JIE.match(l.strip())]),
             len([l for l in ls if BREATH.match(l.strip())]),
             len([l for l in ls if TI.search(l)]),
             len([x for l in ls for x in CARD.findall(l)]), fences,
             sum(len(m.HAS_LAW.findall(l)) for l in ls)))


def apx(ls):
    return len([l for l in ls if l.startswith("## 附錄")])


for name, fn in PAIRS:
    print("■", name)
    b = (ROOT / "_archive/備份/AI清理前" / (fn + "." + BASETAG)).read_bytes()
    bl = b.decode("utf-8").split("\r\n")
    age = "同齡 ✓" if len(bl) == EXPECT[fn] else "★基線已老（帳上作 %d 行，勿據此對照）" % EXPECT[fn]
    print("  基線 .%s・%d 行・SHA %s → %s" % (BASETAG, len(bl), hashlib.sha256(b).hexdigest()[:12], age))
    stat(bl, "一輪後")
    cur = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
    stat(cur, "今正本")
    print("  附錄之篇 %d・迎回之量 +%d 行（今 %d − 一輪後 %d）" % (apx(cur), len(cur) - len(bl), len(cur), len(bl)))
