# -*- coding: utf-8 -*-
"""生活場域軸之覆核（附錄一）：六組之和須 102・一案一歸屬（不重不漏）。
外路第三輪實測：表面 21+19+24+25+8+5＝102，而集合去重唯 100——重號 02・24，缺號 08・09。
故此尺量「去重後之數」與「重／缺之名」，不量各組標題自報之數。
用法：python -X utf8 _work/pairfield.py
"""
import io
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F2 = os.path.join(ROOT, "如法推尋：僧伽憲政、法權審理與修復正義.txt")

L = io.open(F2, "rb").read().decode("utf-8-sig").replace("\r\n", "\n").split("\n")
k0 = [k for k, l in enumerate(L) if u"一、個人修煉領域" in l]
if not k0:
    raise SystemExit(u"附錄一之生活場域軸不在檔內")
groups, titles = [], []
for k in range(k0[0], min(k0[0] + 14, len(L))):
    m = re.match(u"\\* \\*\\*(.+?)（(\\d+) 案）\\*\\*", L[k])
    if m:
        titles.append((m.group(1), int(m.group(2))))
        continue
    if re.match(u"^\\s*〔案例", L[k]):
        groups.append([int(x) for x in re.findall(u"〔案例 (\\d+)〕", L[k])])

print("=" * 66)
print(u"■ 生活場域軸｜標題 %d 組・清單 %d 組" % (len(titles), len(groups)))
declared = sum(n for _, n in titles)
c = Counter(n for g in groups for n in g)
dup = sorted(k for k, v in c.items() if v > 1)
miss = [x for x in range(1, 103) if x not in c]
for (t, n), g in zip(titles, groups):
    flag = u"" if n == len(g) else u"  ← 自報 %d≠實列 %d" % (n, len(g))
    print(u"  %-22s 自報 %2d・實列 %2d%s" % (t[:22], n, len(g), flag))
print(u"  合計：自報 %d・實列 %d・去重 %d" % (declared, sum(len(g) for g in groups), len(c)))
print(u"  重號：%s｜缺號：%s" % (dup or u"無", miss or u"無"))
bad = []
if declared != 102 or sum(len(g) for g in groups) != 102:
    bad.append(u"總數非 102")
if dup:
    bad.append(u"重號 %s" % dup)
if miss:
    bad.append(u"缺號 %s" % miss)
if any(n != len(g) for (_, n), g in zip(titles, groups)):
    bad.append(u"各組自報與實列不合")
if bad:
    print(u"\n✗ 紅：%s" % u"；".join(bad))
    sys.exit(1)
print(u"\n✓ 全綠：102 案一案一歸屬（不重不漏），各組自報與實列相符。")
