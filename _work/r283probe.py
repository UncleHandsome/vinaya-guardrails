# -*- coding: utf-8 -*-
"""283・量：外路第十一報告十二案之今檔現況（只讀不改）。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk  # noqa: E402

BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)
H = re.compile(u'^#{1,6} +(.*)$')
sec, cur = {}, u'卷首'
for i, l in enumerate(LINES):
    m = H.match(l)
    if m:
        cur = m.group(1)[:34]
    sec[i] = cur


def where(key, limit=12, width=150):
    hs = [i for i, l in enumerate(LINES) if key in l]
    print(u'  ◆『%s』%d 見：%s' % (key, len(hs), [i + 1 for i in hs[:limit]]))
    for i in hs[:limit]:
        print(u'      L%d@%s| %s' % (i + 1, sec[i], LINES[i][:width]))
    return hs


print(u'【甲・微型道場之法定人數】')
for k in (u'未滿四人', u'五人以下', u'四人僧', u'微型', u'小廟', u'小道場'):
    where(k, 8, 120)

print(u'【乙・第八章兩處寄生】')
where(u'視訊會議之法權效力', 4, 200)
where(u'數位資產物權法相', 4, 200)
a8 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第八章'))
for i in range(a8, len(LINES)):
    if LINES[i].startswith(u'## ') or LINES[i].startswith(u'### ') or LINES[i].startswith(u'#### '):
        print(u'    L%d| %s' % (i + 1, LINES[i][:70]))
    if i + 1 < len(LINES) and LINES[i + 1].startswith(u'# ') and not LINES[i + 1].startswith(u'# 第八章'):
        break

print(u'【丙・第七章第四節之四署】')
where(u'四法', 6, 220)
where(u'非法足數', 6, 200)
where(u'四署', 6, 160)

print(u'【丁・出堂洗心三事之重複】')
where(u'出堂洗心三事', 6, 120)
where(u'封存案卷', 6, 100)
where(u'消磁', 20, 80)

print(u'【戊・J 標籤】')
for k in (u'J-1', u'J-2', u'J-3', u'J-4', u'案例 J', u'現代深水'):
    where(k, 8, 120)

print(u'【己・附錄五波羅夷喻之衍字】')
where(u'譬如斷人頭', 8, 260)
V = _tk.VINAYA
for k in (u'比丘亦復如是', u'比丘亦如是', u'譬如斷人頭'):
    print(u'  ［語料］『%s』：%d 見' % (k, V.count(k)))
for m in re.finditer(u'譬如斷人頭[^\u3002]{0,40}', V):
    print(u'      語料片段：%s' % m.group(0))

print(u'【庚・目錄之終卷與產器】')
where(u'終卷', 10, 130)
BP = os.path.join(ROOT, u'_print', u'build39.py')
B = io.open(BP, encoding=u'utf-8-sig').read()
print(u'  ◆build39 內『終卷』：%d 見' % B.count(u'終卷'))
for m in re.finditer(u'.{0,90}終卷.{0,90}', B):
    print(u'      %s' % m.group(0).replace(u'\n', u'\\n'))

print(u'【辛・凡例『詳見第八章』之自稱】')
where(u'詳見第八章', 8, 220)
where(u'自註四見', 4, 260)
where(u'屬證據能力之會通', 4, 200)

print(u'【壬・附錄六十五則之歧義】')
where(u'附錄六十五則', 4, 260)

print(u'【癸・代持三軌之稅務與避風港之律源】')
where(u'稅', 12, 90)
where(u'信託登記', 4, 140)
where(u'避風港', 5, 160)
where(u'疑根', 5, 160)
where(u'見聞疑', 8, 120)
for k in (u'無根', u'有根', u'疑'):
    print(u'  ［語料』%s』：%d 見' % (k, V.count(k)))
for m in re.finditer(u'[^。]{0,40}有根[^。]{0,60}', V):
    s = m.group(0)
    if u'謗' in s or u'舉' in s:
        print(u'      語料：%s' % s[:120])
