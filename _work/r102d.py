# -*- coding: utf-8 -*-
"""第 102 輪探針：僅取『引號括出之詞』＋N 見 式宣稱，以逐字口徑復算（可升為不變量之形）。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

DOC = _tk.DOC
LINES = DOC.split("\n")
BOTTOM = _tk.bottom_lines()
PAT = re.compile(u"[『「]([^』「」』]{1,10})[』」**]{0,2}[^0-9、，。；：\n]{0,4}?(\d{1,4})\s*見")
rows = []
for i, l in enumerate(LINES):
    if i in BOTTOM or u"見" not in l:
        continue
    for m in PAT.finditer(l):
        rows.append((i + 1, m.group(1), int(m.group(2))))
bad = []
for ln, term, num in rows:
    a = _tk.term_count(term)
    if a != num:
        bad.append((ln, term, num, a))
print("引號式頻次宣稱 %d 筆；不合 %d 筆" % (len(rows), len(bad)))
for ln, t, n, a in bad:
    print("  L%-6d 『%s』 載 %d 實 %d ｜%s" % (ln, t, n, a, LINES[ln - 1].strip()[:70]))
