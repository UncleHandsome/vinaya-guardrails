# -*- coding: utf-8 -*-
"""283・量（三）：兩款『出堂洗心三事』之全文重疊・第四章第三節之款目與數位證據款之末・四法緣僧之上文・ver38 之 J。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')


def span(start, stops=(u'#### ', u'### ', u'## ', u'# ')):
    i = next(k for k, l in enumerate(LINES) if l.startswith(start))
    lvl = len(start)
    j = i + 1
    while j < len(LINES):
        s = LINES[j]
        if s.startswith(u'#') and any(s.startswith(x) and len(x) <= lvl for x in stops):
            break
        j += 1
    return i, j


a1, e1 = span(u'#### 二、程序終結之消磁宣告（出堂洗心三事）')
a2, e2 = span(u'#### 一、出堂洗心三事（結案當日強制消磁儀軌')
B1 = u'\n'.join(LINES[a1:e1])
B2 = u'\n'.join(LINES[a2:e2])
print(u'【丁】第四章款 L%d..%d・%d 行・%d 字｜第七章款 L%d..%d・%d 行・%d 字' % (
    a1 + 1, e1, e1 - a1, len(B1), a2 + 1, e2, e2 - a2, len(B2)))
s1 = set(re.sub(u'[^\\u4e00-\\u9fff]', u'', B1))
n1 = re.sub(u'[^\\u4e00-\\u9fff]', u'', B1)
n2 = re.sub(u'[^\\u4e00-\\u9fff]', u'', B2)
# 最長公共子串之逐段清單
runs, i = [], 0
while i < len(n1):
    j = i
    best = 0
    while j < len(n1) and n2.find(n1[i:j + 1]) >= 0:
        best = j - i + 1
        j += 1
    if best >= 20:
        runs.append((i, best, n1[i:i + best]))
        i += best
    else:
        i += 1
print(u'  公共長串（≥20 字）：%d 條・共 %d 字（佔第四章款 %d%%）' % (
    len(runs), sum(r[1] for r in runs), 100 * sum(r[1] for r in runs) // max(1, len(n1))))
for r in runs[:8]:
    print(u'   %d 字｜%s……' % (r[1], r[2][:50]))

print(u'【辛】第四章第三節之款目：')
i4 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第四章'))
i5 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第五章'))
s3 = next(i for i in range(i4, i5) if LINES[i].startswith(u'### 第三節'))
n3 = next(i for i in range(s3 + 1, i5) if LINES[i].startswith(u'### '))
print(u'  節界 L%d..%d' % (s3 + 1, n3))
for i in range(s3, n3):
    if LINES[i].startswith(u'#### '):
        print(u'   L%d| %s' % (i + 1, LINES[i][:60]))
for i in range(s3, n3):
    if u'數位' in LINES[i] and LINES[i].startswith(u'##### '):
        print(u'   （數位目）L%d| %s' % (i + 1, LINES[i][:60]))
        for k in range(i, min(i + 14, n3)):
            if LINES[k].strip():
                print(u'      L%d| %s' % (k + 1, LINES[k][:150]))
        break

print(u'【丙附】L3325..3345（受別住圍欄）：')
for i in range(3324, 3346):
    if LINES[i].strip():
        print(u'   L%d| %s' % (i + 1, LINES[i][:150]))

print(u'【戊】ver38 之 J：')
V38 = os.path.join(ROOT, u'_archive', u'舊本', u'ver38四分律_起心動念心智分析框架_修正版.md')
if os.path.exists(V38):
    S = io.open(V38, encoding=u'utf-8-sig').read()
    for k in (u'J-1', u'J-2', u'案例 J', u'附錄J', u'附錄 J', u'現代深水', u'Judicial'):
        print(u'   ver38『%s』：%d' % (k, S.count(k)))
    for m in list(re.finditer(u'[^\\n]{0,80}案例 J[^\\n]{0,80}', S))[:6]:
        print(u'    %s' % m.group(0).replace(u'\n', u' ')[:170])
    for m in list(re.finditer(u'[^\\n]{0,60}附錄 ?J[^\\n]{0,60}', S))[:6]:
        print(u'    %s' % m.group(0).replace(u'\n', u' ')[:150])
else:
    print(u'   ver38 不可讀：%s' % V38)
