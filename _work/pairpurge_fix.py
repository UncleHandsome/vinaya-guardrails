# -*- coding: utf-8 -*-
"""欄內對齊之修復：第三波諸刀於圍欄內換字時未補格者，自備份重放（欄內須補格保欄）而覆之。

只動『圍欄內且寬度與備份不合』之行——一列一行一行修，不整檔換，不動其他內容。
用法：python -X utf8 _work/pairpurge_fix.py [--write]
"""
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
GUTTER = p1.GUTTER
PAIRS = [("F2", "如法推尋：僧伽憲政、法權審理與修復正義.txt", ".pre_purge"),
         ("F1", "起心動念：四分律的心智顯微鏡與唯識解剖.txt", ".pre_purge")]


def dw(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def tokens_for(f):
    out = []
    for src in (p2.TOKEN, p3.TOKEN):
        out += [(o, n) for fn, o, n in src if fn == f]
    for row in p2.LINE:
        if row[0] == f:
            out.append((row[1], row[2]))
    return out


def swap(line, old, new):
    at = line.index(old)
    tail = line[at + len(old):]
    k = len(tail) - len(tail.lstrip(" "))
    if k == 0 and not GUTTER.search(tail):        # 無欄間可守者，直替不補（免生大洞）
        return line[:at] + new + tail
    return line[:at] + new + " " * max(0, k + dw(old) - dw(new)) + tail.lstrip(" ")


def main():
    write = "--write" in sys.argv
    for tag, fn, suf in PAIRS:
        p = ROOT / fn
        bak = (ROOT / "_archive/備份/AI清理前" / (fn + suf)).read_bytes().decode("utf-8").split("\r\n")
        cur = p.read_bytes().decode("utf-8").split("\r\n")
        inside, fixed, drop = False, [], []
        for i in range(min(len(bak), len(cur))):
            s = cur[i].strip()
            if s.startswith(FENCE):
                inside = not inside
                continue
            if not inside or bak[i] == cur[i]:
                continue
            rebuilt = bak[i]
            rebuilt, _gone = p1.strip_parens(rebuilt, True)      # 重放『子』（欄內視欄間而定補格）
            for old, new in tokens_for(fn):
                if old in rebuilt:
                    rebuilt = swap(rebuilt, old, new)
            if not rebuilt.strip():                              # 純外文之標籤行：剥後既空，整行除
                drop.append(i)
                fixed.append((i, cur[i], "(整行除)", dw(bak[i]), 0))
                continue
            if rebuilt != cur[i]:
                fixed.append((i, cur[i], rebuilt, dw(bak[i]), dw(rebuilt)))
                cur[i] = rebuilt
        for i in sorted(drop, reverse=True):
            del cur[i]
        print(f"■ {tag}・欄內重建 {len(fixed)} 行（其中整行除 {len(drop)} 行）")
        for i, o, n, w0, w1 in fixed:
            print(f"    L{i + 1:<6}{'寬' if w0 != w1 else '守'} {w0}→{w1}  故 {o.strip()[:46]}")
            if w0 != w1:
                print(f"                    新 {n.strip()[:46]}")
        if write and fixed:
            raw = (ROOT / fn).read_bytes()
            (ROOT / "_archive/備份/AI清理前" / (fn + ".pre_purgefix")).write_bytes(raw)
            data = "\r\n".join(cur).encode("utf-8")
            p.write_bytes(data)
            print(f"    落盤：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(data).hexdigest()[:12]}")
        elif fixed:
            print("    （試跑：未落盤）")


if __name__ == "__main__":
    main()
