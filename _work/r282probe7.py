# -*- coding: utf-8 -*-
"""282・量（七）：五張集群矩陣之表列今製如何——處斷欄是否一律以 **【 起手、爭點欄是否已無套語。
   若乾淨，即可立為第 34 目（護本轮之口徑，免後人再把戒句貼回速查表）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
HEAD = u'| 案號與事相綱要 | 起心動念（微觀心所歸位） | 核心爭點與邊界標尺 | 佛陀處斷與法效 | 律典原典出處 |'
heads = [i for i, l in enumerate(LINES) if l.strip() == HEAD.strip()]
print(u'矩陣表頭：%d 張 ➔ %s' % (len(heads), [i + 1 for i in heads]))
CASE = re.compile(u'\\| \\*\\*〔案例')
rows = 0
bad3 = []
bad4 = []
seg = []
for h in heads:
    i = h + 2
    n = 0
    while i < len(LINES) and LINES[i].lstrip().startswith(u'|'):
        l = LINES[i]
        if CASE.search(l):
            rows += 1
            n += 1
            cells = [c.strip() for c in l.split(u'|')]
            if len(cells) != 7:
                bad4.append((i + 1, u'欄數 %d' % len(cells)))
                i += 1
                continue
            if u'犯緣與開緣' in cells[3] or cells[3].endswith(u'如何判？'):
                bad3.append((i + 1, cells[3][:40]))
            if not cells[4].startswith(u'**【'):
                bad4.append((i + 1, cells[4][:40]))
        i += 1
    seg.append(n)
print(u'表內案例行：%d 行（各張：%s）' % (rows, seg))
print(u'爭點欄之套語殘跡：%d' % len(bad3))
for x in bad3[:10]:
    print(u'   L%d| %s' % x)
print(u'處斷欄不合式樣：%d' % len(bad4))
for x in bad4[:12]:
    print(u'   L%d| %s' % x)
