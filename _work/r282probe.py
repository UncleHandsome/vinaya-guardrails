# -*- coding: utf-8 -*-
"""282・量：列出第六章矩陣內仍帶『犯緣與開緣之界如何判？』套語之行，印其案綱／心念／出處，
   並印同表內式樣正確之兩行作對照。只讀不改。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
TXT = io.open(BOOK, encoding=u'utf-8-sig').read()
LINES = TXT.split(u'\n')

TPL = u'犯緣與開緣之界如何判？'
print(u'TPL 碼位：%s' % u' '.join(u'%04X' % ord(c) for c in TPL))
rows = [i for i, l in enumerate(LINES) if TPL in l]
print(u'套語行：%d' % len(rows))

CASE = re.compile(u'〔案例 ?0*(\\d+)([^〕]*)〕')
for i in rows:
    m = CASE.search(LINES[i])
    cells = [c.strip() for c in LINES[i].split(u'|')]
    print(u'== L%d 案%s%s (%d 欄)' % (i + 1, m.group(1) if m else u'?',
                                      m.group(2) if m else u'', len(cells)))
    for k in (1, 2, 5):
        print(u'  [%d] %s' % (k, cells[k] if k < len(cells) else u'-'))
    print(u'  [4] %s' % (cells[4] if len(cells) > 4 else u'-',))

# 對照：同表內之好行（含【刑名】式粗體處斷、且無套語）
good = []
for i, l in enumerate(LINES):
    if TPL in l or u'|' not in l:
        continue
    if CASE.search(l) and u'**【' in l and len(l) > 200:
        good.append(i)
print(u'好行候選：%d' % len(good))
for i in good[:3]:
    print(u'== L%d' % (i + 1))
    for k, c in enumerate([x.strip() for x in LINES[i].split(u'|')]):
        print(u'  [%d] %s' % (k, c))
