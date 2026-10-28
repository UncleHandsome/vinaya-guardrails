# -*- coding: utf-8 -*-
"""簡形之口徑共器（雙子星兩冊）：名單取 `_simpmap.MAP` ∪ `_simpdict.MAP` 減『几』加盯形 `WATCH`，
   再護一道——**引號之內而語料自有其形者不為病**（大正藏原形『並』『衆』之類，非刀之誤）。
   此與 ver39 冊 `v39chk` 之『減語料所見之形』同其精神，唯更緊：以『字在引號內』為限。
   六支器共用，勿再各抄口徑（235・238 輪之誡）。"""
import importlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import _tk  # noqa: E402

_SM = importlib.import_module("_simpmap")
_SD = importlib.import_module("_simpdict")
FALSE_SIMP = set("几")
# 兩張字典之盲點（第十一波 A6 之獲）：『堅守』之簡形 U+575A 向不入名單，歷輪簡形尺遂全綠而病在冊。
# 此類『簡形而不成對入典』之常字，須手工盯形；『后・台・干・里・面・服・沉』之屬乃一簡多繁，
# 直入即誤傷正文（后＝皇后・干＝干犯・里＝市里），故只盯『绝對不得作正字用』者，餘歸目驗。
WATCH = set("坚")
SIMPLE = (set(_SM.MAP) | set(_SD.MAP)) - FALSE_SIMP | WATCH
CORPUS_CHARS = set(_tk.VINAYA)
for _v in _tk.OTHER.values():
    CORPUS_CHARS |= set(_v)
SPAN = re.compile(r"「[^」]*」|『[^』]*』|“[^”]*”")


def quote_spans(line):
    return [(m.start(), m.end()) for m in SPAN.finditer(line)]


def hits(line):
    """回該行須治之簡形字（去重排序）；居引號之內且語料自有其形者，乃大正藏原形，不為病。"""
    sp = quote_spans(line)
    out = set()
    for i, c in enumerate(line):
        if c not in SIMPLE:
            continue
        if c in CORPUS_CHARS and any(a <= i < b for a, b in sp):
            continue
        out.add(c)
    return "".join(sorted(out))


def flag(line):
    """True ＝此行尚有真簡形。"""
    return bool(hits(line))
