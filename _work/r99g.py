# -*- coding: utf-8 -*-
"""第 98 輪套改：一、拉丁比較詞 vs 改漢語「對」（僅行款與標題，表格與第九章不預）；
二、括注自我重述六處削平。"""
import io, os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "ver38四分律_起心動念心智分析框架_修正版.md")
s = io.open(MD, encoding="utf-8").read()
lines = s.split("\n")
c9 = next(i for i, l in enumerate(lines) if l.startswith("# 第九章"))
c9e = next(i for i, l in enumerate(lines) if i > c9 and l.startswith("# "))
log = []
inb = False
for i, l in enumerate(lines):
    if l.startswith("```"):
        inb = not inb
        continue
    if inb or c9 <= i < c9e or l.lstrip().startswith("|"):
        continue
    if "vs" not in l and "VS" not in l:
        continue
    n = re.sub(r"(?<![A-Za-z])vs(?![A-Za-z])", "對", l, flags=re.I)
    if n != l:
        lines[i] = n
        log.append("L%d vs→對\n   舊 %s\n   新 %s" % (i + 1, l.strip()[:74], n.strip()[:74]))
s = "\n".join(lines)

def rep(old, new, tag):
    global s
    k = s.count(old)
    log.append("%s %s（命中 %d）" % ("OK  " if k == 1 else ("MULT" if k > 1 else "MISS"), tag, k))
    if k == 1:
        s = s.replace(old, new, 1)

rep("#### 一、擯出羯磨 對 遮不至白衣家羯磨（下意羯磨）之要件劃界",
    "#### 一、擯出羯磨與遮不至白衣家羯磨之要件劃界", "2 擯出劃界標題去複alias")
rep("* **明知故犯（故犯）**", "* **明知故犯**", "3 削同義括注")
rep("* **心智定性（以心定性）**", "* **心智定性**", "4 削以心定性")
rep("* **事相定量（以事定量）**", "* **事相定量**", "5 削以事定量")
rep("防衛姿態（閘門四：防衛姿態）", "防衛姿態（閘門四）", "6 削閘門四重述")
rep("##### （三）終環入無事（問[11]至問[16]：解脫閉環與歸家無事）",
    "##### （三）終環入無事（問[11]至問[16]）", "7 削問次標題重述")
rep("**黃門（生、形殘、妬、變、半月五種黃門）**", "**黃門（生、形殘、妬、變、半月五種）**",
    "8 削五種黃門重述")

io.open(MD, "w", encoding="utf-8").write(s)
io.open(os.path.join(ROOT, "_work", "r99g.txt"), "w", encoding="utf-8").write("\n".join(log) + "\n")
sys.stdout.write("\n".join(log) + "\n")
