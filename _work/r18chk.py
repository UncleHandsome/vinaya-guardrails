# -*- coding: utf-8 -*-
"""第 51 輪覆核：六枚去式樣之語是否俱已改掛『』（並核印面錨數之減）。"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, ".")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BOOK = HP.SRC
t = io.open(BOOK, encoding="utf-8", newline="").read()
KEYS = [u"行為心理防禦工事圖", u"城郭宮殿之喻", u"選擇架構（Choice Architecture）",
        u"國王鎮守的邊疆重鎮", u"兵臨城下的百萬敵軍", u"層層設防、環環相扣的幾何防禦工程"]
PAT = re.compile(u"「\\*\\*([^」\\n]{2,60})\\*\\*」|\\*\\*「([^」\\n]{2,60})」\\*\\*")
signed = set()
for m in PAT.finditer(t):
    signed.add((m.group(1) or m.group(2)).strip())
for k in KEYS:
    a = t.count(u"『" + k + u"』")
    b = sum(1 for s in signed if s == k or k in s)
    print(u"%-22s 『』%d ｜ 仍掛逐字式樣 %d" % (k, a, b))
print(u"全書粗體＋引號式樣（去重後）：%d 種" % len(signed))
