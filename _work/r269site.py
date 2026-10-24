# -*- coding: utf-8 -*-
"""269 輪・量二：今冊確存之四項（解耦・甲乙丙・存檔卡・自省記錄）逐-site 明細，供分刀與呈裁。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')


def chap_of(i):
    ch = u'卷首'
    for k in range(i + 1):
        m = re.match(u'^# (第.{1,3}章|結語|終卷|附錄[一二三四五六])', L[k])
        if m:
            ch = m.group(1)
    return ch


def hits(kw):
    return [(i + 1, chap_of(i), L[i].strip()) for i, l in enumerate(L) if kw in l]


print(u'── 一・解耦（逐 site）──')
for n, c, s in hits(u'解耦'):
    print(u'  L%-5d %-8s %s' % (n, c, s[:132]))
print(u'\n── 二・甲／乙／丙級 與 三級判準（逐 site）──')
for kw in [u'甲級', u'乙級', u'丙級', u'三級判準', u'以丙代甲', u'以乙代甲', u'以甲代', u'除偏鏡']:
    for n, c, s in hits(kw)[:4]:
        print(u'  %-6s L%-5d %-8s %s' % (kw, n, c, s[:118]))
print(u'\n── 三・存檔卡・親簽・勾選框 ──')
for kw in [u'存檔卡', u'親簽', u'[ ]']:
    hh = hits(kw)
    print(u'  「%s」共 %d 見' % (kw, len(hh)))
    by = {}
    for n, c, s in hh:
        by[c] = by.get(c, 0) + 1
    print(u'      分佈：%s' % u'・'.join(u'%s%d' % (k, v) for k, v in sorted(by.items())))
    for n, c, s in hh[:3]:
        print(u'      L%-5d %-8s %s' % (n, c, s[:110]))
print(u'\n── 四・自省記錄一條之全文（含其上下各一行）──')
for i, l in enumerate(L):
    if u'自省記錄' in l and i > 500:
        for k in range(max(0, i - 2), min(len(L), i + 3)):
            print(u'  L%-5d %s' % (k + 1, L[k][:150]))
print(u'\n── 五・凡例今存第幾節（括號之規範還在否）──')
for i, l in enumerate(L[:320]):
    if l.startswith(u'### ') and i > 230:
        print(u'  L%-5d %s' % (i + 1, l[:60]))
