# -*- coding: utf-8 -*-
"""第 49 輪修補二：凡例款①立其判別、甲類五處去逐字式樣（署名之文不得借律文之標）。"""
import os as _hp_os, sys as _hp_sys; _hp_sys.path.insert(0, _hp_os.path.dirname(_hp_os.path.dirname(_hp_os.path.abspath(__file__)))); import hulan_path as HP  # hulan-path
import io
import re
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "_work")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOOK = HP.SRC
NL = chr(13) + chr(10)
GO = u"--go" in sys.argv
raw = io.open(BOOK, encoding="utf-8", newline="").read()
L = raw.split(NL)
n0 = len(L)
NEWTXT = []


def sub(idx, old, new, tag):
    t = L[idx - 1]
    assert t.count(old) == 1, (u"命中數：" + tag, idx, t.count(old))
    L[idx - 1] = t.replace(old, new)
    NEWTXT.append(new)
    print(u"改 %s @L%d" % (tag, idx))


# ── 凡例款①：加判別句（名字與評語之粗體不作逐字宣稱；署名者另標） ──
OLD1 = (u"未加粗體的引號，或為術語標注，或為本書的今語與敘事，不構成逐字的宣稱——"
        u"唯篇末之歷條總表（唯全本有之）所收戒文不加粗體而仍是逐字，其例見該篇凡例。")
NEW1 = (u"未加粗體的引號，或為術語標注，或為本書的今語與敘事，不構成逐字的宣稱——"
        u"唯篇末之歷條總表（唯全本有之）所收戒文不加粗體而仍是逐字，其例見該篇凡例。"
        u"**判別之法：要作逐字宣稱的，其文讀出來必是一句律文，不是一個名字；"
        u"粗體若只加在戒名、喻名、術語或本書的評語上（如『飲酒戒』『動態雷達』之類），只作強調，不作逐字之宣稱。**"
        u"凡出他師他典者，另以『義引』『大意』『義譯』『括旨』如實標之，不在此例。")
sub(68, OLD1, NEW1, u"凡例款①、立判別之法")

# ── 甲類一：L951 三喻名（同句署《雜阿含》《中阿含》《行事鈔》） ──
sub(951, u"比作一座**「國王鎮守的邊疆重鎮」**", u"比作一座『國王鎮守的邊疆重鎮』", u"三章、喻名一")
sub(951, u"將內心的貪愛、瞋恨、放逸比作**「兵臨城下的百萬敵軍」**",
    u"將內心的貪愛、瞋恨、放逸比作『兵臨城下的百萬敵軍』", u"三章、喻名二")
sub(951, u"就是一套**「層層設防、環環相扣的幾何防禦工程」**。",
    u"就是一套『層層設防、環環相扣的幾何防禦工程』——**這三個名字是本書撮舉之喻，非彼經論之現成句。**",
    u"三章、喻名三並如實標")

# ── 甲類二：L957「城郭宮殿之喻」 ──
sub(957, u"留下了著名的**「城郭宮殿之喻」**。", u"留下了著名的『城郭宮殿之喻』（此四字的喻名出後人之撮舉）。",
    u"三章、喻名歸實")

# ── 甲類三：L6365 西人術語之譯名 ──
sub(6365, u"提出了著名的**「選擇架構（Choice Architecture）」**理論：",
    u"提出了著名的『選擇架構』（Choice Architecture）理論：", u"十八章、譯名去式樣")

# ── 自護：簡形、粗體成對、無嘆號 ──
from _simpdict import MAP as SIMP  # noqa: E402
mid = chr(0x30FB)
bad = sorted({c for t in NEWTXT for c in t if c in SIMP})
assert not bad, [(c, SIMP[c], hex(ord(c))) for c in bad]
for i, t in enumerate(L):
    assert t.count(u"**") % 2 == 0, (u"粗體不成對 @L%d" % (i + 1), t[:80])
    assert mid not in t, (u"日式中黑 @L%d" % (i + 1), t[:60])
assert len(L) == n0, (u"行數須不變", len(L), n0)
out = NL.join(L)
assert out.count(chr(13)) == len(L) - 1
print(u"行數 %d ｜ CR %d" % (len(L), out.count(chr(13))))
if GO:
    io.open(BOOK, "w", encoding="utf-8", newline="").write(out)
    print(u"已寫入")
else:
    print(u"（試跑，未寫入）")
