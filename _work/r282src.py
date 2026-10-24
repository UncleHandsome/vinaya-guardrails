# -*- coding: utf-8 -*-
"""282・量：印出二十五案在附錄四之原典卡全文（作為重寫爭點／處斷欄之唯一依據）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
CASES = [3, 17, 35, 71, 73, 60, 68, 70, 72, 96, 99, 40, 59, 61, 62, 64, 65, 66, 67, 69, 92, 94, 95, 100, 58]
A4 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄四'))
A5 = next(i for i, l in enumerate(LINES) if i > A4 and l.startswith(u'# 附錄'))
PAT = re.compile(u'\u3014案例[^\u3014\u3015]*\u3015')

def nums(s):
    out = set()
    for tag in PAT.findall(s):
        for d in re.findall(u'(\\d+)', tag):
            out.add(int(d))
    return out

for n in CASES:
    got = []
    for i in range(A4, A5):
        if n in nums(LINES[i]):
            got.append(LINES[i])
    print(u'@@@ 案%d 附錄四 %d 行' % (n, len(got)))
    for g in got:
        print(g)
    print(u'')
