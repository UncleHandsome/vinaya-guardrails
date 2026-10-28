# -*- coding: utf-8 -*-
"""語料覆核：外路所擬之『律藏本有替代名相』須先在本地語料見形，否則不得貼上（偽託律據之戒）。

用法：python -X utf8 _work/pairtk_terms.py
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
sys.path.insert(0, str(ROOT))
tk = importlib.import_module("_tk")

TERMS = [
    "所不制", "不應制", "所制", "不應卻", "不制",
    "見罪不遮", "屏處", "獨處", "伴", "俱行", "同行",
    "草覆", "破草", "糞", "燃火", "賊", "深穴", "夜分",
    "息諍", "滅諍", "還淨", "自性", "無事",
    "邪命", "誑", "矯現", "威儀", "五如法", "現前毘尼", "不自言",
    "染污惡作", "惡作", "動發勝思", "作意", "正念", "護根", "根門",
    "朋黨", "黨援", "別眾", "法性", "如法", "如草覆地",
    "見聞疑", "三聞", "行舍羅", "與欲", "自恣", "布薩", "說戒",
    "更發", "前罪", "業道", "離處", "五錢", "滿五錢",
]
CORPUS = tk.VINAYA_SEP
for t in TERMS:
    n = CORPUS.count(tk.norm_sep(t))
    print("%-8s 語料 %4d 見%s" % (t, n, "" if n else "　◆ 語料無此形——不得據為『律藏本有』"))
