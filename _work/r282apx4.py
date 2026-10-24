# -*- coding: utf-8 -*-
"""282・量：二十五案之載體清冊（含附錄四有無卡）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')

CASES = [3, 17, 35, 71, 73, 60, 68, 70, 72, 96, 99, 40, 59, 61, 62, 64, 65, 66, 67, 69, 92, 94, 95, 100, 58]
HEAD = re.compile(u'^#{1,6} +(.*)$')
# 各行之章／節屬
sec, cur = {}, u'卷首'
for i, l in enumerate(LINES):
    m = HEAD.match(l)
    if m:
        cur = m.group(1)[:30]
    sec[i] = cur

apx4 = [i for i, l in enumerate(LINES) if HEAD.match(l) and u'附錄四' in l]
start4 = apx4[0] if apx4 else len(LINES)
print(u'附錄四起於 L%d：%s' % (start4 + 1, LINES[start4][:40]))

pat = re.compile(u'〔案例 0*(\\d+)[^〕]*〕')
for n in CASES:
    hits = [i for i, l in enumerate(LINES) if n in [int(x) for x in pat.findall(l)]]
    in4 = [i for i in hits if i >= start4]
    print(u'案%-3d 共 %2d 載體・附錄四 %s・%s' % (
        n, len(hits), len(in4),
        u'｜'.join(u'L%d@%s' % (i + 1, sec[i]) for i in hits[:8])))
