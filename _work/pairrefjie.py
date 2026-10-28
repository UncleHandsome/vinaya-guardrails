# -*- coding: utf-8 -*-
"""指針之檢：刀後若重排「第N節／一、二、三」之序，先數書中是否有跨段之節級引用。"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F2 = ROOT / "如法推尋：僧伽憲政、法權審理與修復正義.txt"
F1 = ROOT / "起心動念：四分律的心智顯微鏡與唯識解剖.txt"

RX_JIE = re.compile(r"第[〇一二三四五六七八九十]+節")
HEAD = re.compile(r"^#{1,6}\s")

for tag, p in (("F2 法制卷", F2), ("F1 心法卷", F1)):
    lines = p.read_text(encoding="utf-8").split("\n")
    hits = []
    for i, l in enumerate(lines, 1):
        if RX_JIE.search(l):
            kind = "標題" if HEAD.match(l.strip()) else ("指針" if re.search(r"(見|參|詳|前|後|上文|下文|第[一二三四五]篇).{0,18}第[〇一二三四五六七八九十]+節", l) or not HEAD.match(l.strip()) else "?")
            hits.append((i, kind, l.strip()[:74]))
    print("=" * 70)
    print(f"■ {tag}：『第N節』現形 {len(hits)} 行（其中非標題者 {sum(1 for h in hits if h[1] != '標題')} 行）")
    for i, kind, t in hits:
        if kind != "標題":
            print(f"    L{i} [{kind}] {t}")
