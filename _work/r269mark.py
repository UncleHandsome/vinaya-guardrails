# -*- coding: utf-8 -*-
"""269 輪・量三：① 凡例第二節所宣之標記（◎原典・〔名相〕）在今冊**是否真用**（宣稱-vs-實態）；
   ② 甲／乙／丙作為**層級代號**之全部落點；③ 『保密義務』是否唯 L2347 一处（呈裁之據）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
BOOK = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read()
L = BOOK.split(u'\n')


def chap_of(i):
    ch = u'卷首'
    for k in range(i + 1):
        m = re.match(u'^# (第.{1,3}章|結語|終卷|附錄[一二三四五六])', L[k])
        if m:
            ch = m.group(1)
    return ch


print(u'── ① 凡例所宣之標記，今冊實況 ──')
for kw in [u'◎', u'◈', u'◎原典', u'原典層', u'判準層', u'名相〕', u'〔名相〕']:
    print(u'   「%s」%d 見' % (kw, BOOK.count(kw)))
print(u'   含「◎」之行：')
for i, l in enumerate(L):
    if u'◎' in l:
        print(u'      L%-5d %-8s %s' % (i + 1, chap_of(i), l.strip()[:96]))

print(u'\n── ② 〔…〕用作『名相標籤』之形（非案例卡）──')
pat = re.compile(u'〔([^〕]{2,14})〕')
cases = 0
other = {}
for i, l in enumerate(L):
    for m in pat.finditer(l):
        s = m.group(1)
        if re.match(u'^(案例|補遺)', s.strip()):
            cases += 1
        else:
            other.setdefault(s.strip()[:12], []).append(i + 1)
print(u'   案例／補遺之〔〕：%d 見・其他〔〕：%d 種' % (cases, len(other)))
for k, v in sorted(other.items(), key=lambda x: -len(x[1]))[:14]:
    print(u'      〔%-14s〕%d 見  例 L%d' % (k, len(v), v[0]))

print(u'\n── ③ 甲／乙／丙 作層級代號之全部落點 ──')
LEV = re.compile(u'(?:[甲乙丙]級|代[甲乙]|廢甲|甲乙丙|[丙乙]代[甲])')
tot = 0
for i, l in enumerate(L):
    for m in set(LEV.findall(l)):
        tot += 1
        print(u'   L%-5d %-8s %-8s ｜ %s' % (i + 1, chap_of(i), m, l.strip()[:88]))
print(u'   合 %d 處' % tot)

print(u'\n── ④ 『保密義務』與『自言治』之分工（呈裁之據）──')
for kw in [u'保密義務', u'保密', u'自言治']:
    print(u'   「%s」%d 見' % (kw, BOOK.count(kw)))
    for i, l in enumerate(L):
        if kw in l and BOOK.count(kw) <= 6:
            print(u'      L%-5d %-8s %s' % (i + 1, chap_of(i), l.strip()[:92]))
