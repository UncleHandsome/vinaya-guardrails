# -*- coding: utf-8 -*-
"""282・量（五）：第七章第二節四軸之重複號與孤行・第八章之節題與隱私段・『當然／自動』之去職宣稱・附錄三人名表全貌。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)


def rng(mark, lvl=u'# '):
    a = next((i for i, l in enumerate(LINES) if l.startswith(lvl) and mark in l), None)
    return a


# 甲・第七章第二節全貌
a = rng(u'第二節　判例四維', u'### ')
b = next(i for i in range(a + 1, len(LINES)) if LINES[i].startswith(u'### ') or LINES[i].startswith(u'# '))
print(u'== 第七章第二節 L%d..%d（%d 行）' % (a + 1, b + 1, b - a))
for i in range(a, b):
    l = LINES[i]
    if l.startswith(u'#'):
        print(u'  L%d %s' % (i + 1, l[:70]))
NUM = re.compile(u'案例 0*(\\d+)')
for i in range(a, b):
    l = LINES[i]
    ns = [int(x) for x in NUM.findall(l)]
    dup = sorted({n for n in ns if ns.count(n) > 1})
    if dup:
        print(u'  [重號] L%d 案%s| %s' % (i + 1, dup, l[:200]))
# 孤行：節末之單一短行
print(u'  節末五行：')
for i in range(b - 5, b):
    print(u'    L%d| %s' % (i + 1, LINES[i][:170]))

# 乙・第八章節題
a8 = rng(u'第八章')
b8 = next(i for i in range(a8 + 1, len(LINES)) if LINES[i].startswith(u'# '))
print(u'== 第八章 L%d..%d 之節題：' % (a8 + 1, b8 + 1))
for i in range(a8, b8):
    if LINES[i].startswith(u'## ') or LINES[i].startswith(u'### '):
        print(u'  L%d %s' % (i + 1, LINES[i][:70]))

# 丙・隱私與個資之現文
for w in (u'隱私', u'個資', u'去識別', u'病歷'):
    for i, l in enumerate(LINES):
        if w in l:
            print(u'  [%s] L%d| %s' % (w, i + 1, l[:190]))

# 丁・『當然』『自動』之去職宣稱
for w in (u'當然', u'自動', u'不待', u'无需', u'不須'):
    hs = [(i + 1, LINES[i][:90]) for i, l in enumerate(LINES) if w in l]
    print(u'  [%s]：%d 處' % (w, len(hs)))
    for h in hs[:14]:
        print(u'      L%d| %s' % h)

# 戊・附錄三人名表全貌
a3 = rng(u'二、律典原生人名')
b3 = next(i for i in range(a3 + 1, len(LINES)) if LINES[i].startswith(u'#'))
print(u'== 附錄三人名表 L%d..%d' % (a3 + 1, b3 + 1))
for i in range(a3, b3):
    print(u'  L%d| %s' % (i + 1, LINES[i][:130]))
for k in (u'25 位', u'27 位', u'29 位', u'十六位', u'二十五'):
    print(u'  宣稱[%s]：%d 處 %s' % (k, T.count(k), [i + 1 for i, l in enumerate(LINES) if k in l][:6]))
