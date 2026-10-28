# -*- coding: utf-8 -*-
"""第三波诸刀之『重放器』：自 .pre_purge 備份起，以修正後之規則一次重放子・丑・寅・卯諸刀。

所以立此器：器改一寸（剥外文後之『空斜體』清理規則太貪，誤食 `* **粗體**` 之起手法則；
IAST 判式改碼位，免誤剥 Daśavarga・Sparśa），書上之傷須以同一法源重生成，不可逐行手補——
『凡有產生器之區塊，筆須落在產生器』（舊戒）。
用法：python -X utf8 _work/pairpurge_replay.py [--write] [--diff]
"""
import difflib
import hashlib
import importlib
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
importlib.import_module("pairdelaw")
p1 = importlib.import_module("pairpurge")
p2 = importlib.import_module("pairpurge2")
p3 = importlib.import_module("pairpurge3")

FENCE = "```"
FILES = [("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt"),
         ("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt")]


def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def flags(ls):
    out, inside = [], False
    for l in ls:
        if l.strip().startswith(FENCE):
            out.append(inside)
            inside = not inside
        else:
            out.append(inside)
    return out


def tokens_for(f):
    rows = [(o, n) for fn, o, n in p2.TOKEN if fn == f]
    rows += [(o, n) for fn, o, n in p3.TOKEN if fn == f]
    rows += [(r[1], r[2]) for r in p2.LINE if r[0] == f]
    return rows


def swap(line, old, new, in_fence):
    at = line.index(old)
    tail = line[at + len(old):]
    if not in_fence:
        return line[:at] + new + tail
    k = len(tail) - len(tail.lstrip(" "))
    if k == 0 and not p1.GUTTER.search(tail):
        return line[:at] + new + tail
    return line[:at] + new + " " * max(1, k + dw(old) - dw(new)) + tail.lstrip(" ")


def main():
    write = "--write" in sys.argv
    for tag, fn in FILES:
        bak = (ROOT / "_archive/備份/AI清理前" / (fn + ".pre_purge")).read_bytes().decode("utf-8").split("\r\n")
        cur = (ROOT / fn).read_bytes().decode("utf-8").split("\r\n")
        fb = flags(bak)
        rebuilt, void = [], 0
        for i, l in enumerate(bak):
            if l.strip().startswith(FENCE):
                rebuilt.append(l)
                continue
            nl, _ = p1.strip_parens(l, fb[i])
            for old, new in tokens_for(fn):
                if old in nl:
                    nl = swap(nl, old, new, fb[i])
            if fb[i] and not nl.strip() and l.strip():
                void += 1                       # 圍欄內之純外文標籤行：剥後既空，整行除
                continue
            rebuilt.append(nl)
        diff = [(i + 1, cur[i] if i < len(cur) else "", rebuilt[i])
                for i in range(len(rebuilt)) if i >= len(cur) or cur[i] != rebuilt[i]]
        print("=" * 74)
        print(f"■ {tag}・重放 {len(bak)} → {len(rebuilt)} 行（整行除 {void}）・與今檔之異 {len(diff)} 行")
        for i, o, n in diff[:24]:
            print(f"    L{i:<6} 今 {o.strip()[:56]}\n           放 {n.strip()[:56]}")
        if write:
            p = ROOT / fn
            raw = p.read_bytes()
            (ROOT / "_archive/備份/AI清理前" / (fn + ".pre_replay")).write_bytes(raw)
            data = "\r\n".join(rebuilt).encode("utf-8")
            p.write_bytes(data)
            print(f"    落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}"
                  f"・行 {len(raw.decode('utf-8').split(chr(13)+chr(10)))} → {len(rebuilt)}")




main()
