# -*- coding: utf-8 -*-
"""第三波『去延伸名相』·卯刀：殘留之『公訴・維度・破罐破摔・前額葉・適應障礙』歸律語。

承 pairpurge（子・外文括號）與 pairpurge2（丑・詞級／寅・句級）。
圍欄內之換字須補格保欄（口徑 W/F/A＝2），並自印管轄（動行・換前後之數）。
用法：python -X utf8 _work/pairpurge3.py [--write]
"""
import hashlib
import re
import pairsimp as PS  # noqa: E402
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "_work"))
import importlib                                            # noqa: E402
m = importlib.import_module("pairdelaw")
_simpmap = importlib.import_module("_simpmap")
_simpdict = importlib.import_module("_simpdict")

F2 = "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = "起心動念：四分律的心智顯微鏡與唯識解剖.txt"
FILES = [F2, F1]
TOKEN = [
    (F2, "對抗世俗干預與公訴分流", "對抗世俗干預與王法分流"),
    (F2, "依法啟動公訴通報優先", "依法啟動王法通報優先"),
    (F2, "**轉化為客觀公訴**", "**轉化為客觀告發**"),
    (F2, "公訴刑事重罪之世俗法定通報義務", "王法重罪之世俗通報義務"),
    (F2, "必須經受五維度的完整檢驗", "必須經受五個層面的完整檢驗"),
    (F2, "| 檢驗維度 |", "| 檢驗之目 |"),
    (F2, "| 五德維度 |", "| 五德之目 |"),
    (F2, "滿足維度 A）", "甲軸具足）"),
    (F2, "滿足維度 B）", "乙軸具足）"),
    (F2, "【維度 A：壇上作法僧", "【甲軸：壇上作法僧"),
    (F2, "【維度 B：壇外常住僧", "【乙軸：壇外常住僧"),
    (F2, "適應障礙", "心疾"),
    (F1, "| 維度 |", "| 層面 |"),
    (F1, "世俗公訴優先", "世俗王法優先"),
    (F1, "涉及重大公訴犯罪", "涉及重大王法之罪"),
    (F1, "**公訴刑案國法優先**：凡涉世俗公訴重罪，出世內部程序退讓，刑事通報優先",
     "**王法刑案國法優先**：凡涉世俗王法重罪，出世內部程序退讓，王法通報優先"),
    (F1, "發動第二次公訴", "發動第二次告發"),
    (F1, "前額葉理性意志被極限恐懼劫持", "理性之意志為極度驚怖所制"),
    (F1, "自暴自棄的破罐破摔", "自暴自棄之自棄滑坡"),
    (F1, "索性破罐破摔", "索性自暴自棄"),
]


def dwidth(s):
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F", "A") else 1 for c in s)


def swap(line, old, new, in_fence):
    at = line.index(old)
    tail = line[at + len(old):]
    out = line[:at] + new + tail
    if in_fence:
        k = len(tail) - len(tail.lstrip(" "))
        need = max(0, k + dwidth(old) - dwidth(new))
        out = line[:at] + new + " " * need + tail.lstrip(" ")
    return out


def main():
    write = "--write" in sys.argv
    SIMPLE = (set(_simpmap.MAP) | set(_simpdict.MAP)) - set("几")
    errs, ledger, plans = [], [], []
    for f in FILES:
        raw = (ROOT / f).read_bytes()
        lines = raw.decode("utf-8").split("\r\n")
        fence = m.fence_mask(lines)
        print("=" * 74)
        print("■", f)
        for fn, old, new in [(x[0], x[1], x[2]) for x in TOKEN if x[0] == f]:
            for c in set(new) & SIMPLE:
                errs.append(f"{f[:6]}・新字簡形：{c}｜{new[:18]}")
            hits = [i for i, l in enumerate(lines) if old in l]
            if not hits:
                continue                      # 已竟：今冊 0 見，非病（刀可重入之義）
            for i in hits:
                o = lines[i]
                lines[i] = swap(o, old, new, fence[i])
                if fence[i] and dwidth(lines[i]) != dwidth(o):
                    errs.append(f"{f[:6]}・欄內寬不合 L{i + 1}：{dwidth(o)}→{dwidth(lines[i])}")
                ledger.append(f"{f}\tL{i + 1}\t卯・詞級\t{old} → {new}｜{lines[i].strip()[:36]}")
            rest = sum(l.count(old) for l in lines)
            print(f"  卯 『{old[:22]}』→『{new[:22]}』：動行 {len(hits)}・換後餘 {rest} 見")
        simp = [(i + 1, PS.hits(l), l.strip()[:36])
                for i, l in enumerate(lines) if PS.flag(l)]
        if simp:
            errs.append(f"{f[:6]}・刀後簡形 {len(simp)} 行：{simp[:2]}")
        plans.append((f, raw, lines))
    for e in errs:
        print("  ✗", e)
    if errs:
        print("★有誤 → 兩冊俱不落盤")
        return
    (ROOT / "_work" / "pairpurge3_cuts.txt").write_text("\n".join(ledger) + "\n", encoding="utf-8")
    print(f"\n刀口清冊 {len(ledger)} 行 → _work/pairpurge3_cuts.txt")
    for f, raw, lines in plans:
        out = "\r\n".join(lines).encode("utf-8")
        if not write:
            print(f"  {f[:12]}…・試跑未落盤")
            continue
        bak = ROOT / "_archive" / "備份" / "AI清理前" / (f + ".pre_purge3")
        bak.write_bytes(raw)
        (ROOT / f).write_bytes(out)
        print(f"  落盤 {f[:12]}…：SHA {hashlib.sha256(raw).hexdigest()[:12]} → {hashlib.sha256(out).hexdigest()[:12]}")


if __name__ == "__main__":
    main()
