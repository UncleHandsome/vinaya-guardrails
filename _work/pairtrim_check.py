# -*- coding: utf-8 -*-
"""刀後之雨掃：簡形・遺留法名・殘存科技/公文/軟體名・呼吸之歸位。一器四目，俱印實數。"""
import importlib
import pairsimp as PS  # noqa: E402
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
m = importlib.import_module("pairdelaw")
sm = importlib.import_module("_simpmap")
sd = importlib.import_module("_simpdict")
SIMPLE = (set(sm.MAP) | set(sd.MAP)) - set("几")

FILES = ["如法推尋：僧伽憲政、法權審理與修復正義.txt",
         "起心動念：四分律的心智顯微鏡與唯識解剖.txt"]
SOFT = re.compile(r"Zoom|Teams|LINE|Line|Slack|微信|WhatsApp|YouTube|臉書|Deepfake|深偽|演算法|AI ")
FORM = re.compile(r"法審字第|\[\s+\]|□|簽章|署押|戒臘：|_____")
LAWY = m.HAS_LAW

for fn in FILES:
    ls = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
    simp = [(i + 1, PS.hits(l), l.strip()[:50])
            for i, l in enumerate(ls) if PS.flag(l)]
    soft = [(i + 1, l.strip()[:60]) for i, l in enumerate(ls) if SOFT.search(l)]
    form = [(i + 1, l.strip()[:60]) for i, l in enumerate(ls) if FORM.search(l)]
    law = sum(len(LAWY.findall(l)) for l in ls)
    print("=" * 72)
    print("■", fn[:20], "…・行", len(ls))
    print(f"  簡形 {len(simp)} 行｜科技與軟體名 {len(soft)} 行｜公文表格之跡 {len(form)} 行｜法名／制度名 {law} 見")
    for a, t in soft:
        print(f"      科技 L{a}|{t}")
    for a, t in form:
        print(f"      公文 L{a}|{t}")
    for i, s, t in simp:
        print(f"      簡形 L{i} [{s}] {t}")
