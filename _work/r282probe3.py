# -*- coding: utf-8 -*-
"""282・量（三）：語料之篇名定位・第七章第二節之尾・第八章之解任與搜查・附錄六之出處・壇經上下文。"""
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

print(u'== _tk 之路徑：%s' % [x for x in dir(_tk) if not x.startswith('_')][:24])
V = _tk.VINAYA
print(u'語料總長：%d' % len(V))

# 一・案25／案69 之語料切片與其左近之篇名（犍度・分・法）
PIAN = re.compile(u'(第[一二三四五六七八九十]+分|[\\u4e00-\\u9fff]{2,6}犍度|波逸提法|僧殘法|波羅夷法|受戒犍度)')


def near(txt, key, span=2600):
    i = txt.find(key)
    if i < 0:
        return None
    win = txt[max(0, i - span):i + 80]
    hits = [(m.start(), m.group(0)) for m in PIAN.finditer(win)]
    return (i, hits[-6:])


for lab, key in ((u'案25 乞六夜摩那埵', u'今從僧乞六夜摩那埵'),
                 (u'案25 犯僧殘不覆藏', u'犯僧殘罪不覆藏'),
                 (u'案69 看門相', u'應看巷相'),
                 (u'案69 不看門相便入', u'不看門相便入')):
    print(u'-- %s：%s' % (lab, near(V, key)))

# 二・卷界之證據：語料內是否有『卷第X』之題？
print(u'語料內『卷第』：%d・『四分律卷』：%d' % (V.count(u'卷第'), V.count(u'四分律卷')))

# 三・第七章第二節之尾（心所軸段末）
i7 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第七章'))
s2 = [i for i in range(i7, len(LINES)) if LINES[i].startswith(u'## ') and u'第二節' in LINES[i]]
print(u'== 第七章第二節：%s' % [(i + 1, LINES[i][:30]) for i in s2])
if s2:
    h = s2[0]
    nxt = next((i for i in range(h + 1, len(LINES)) if LINES[i].startswith(u'## ')), len(LINES))
    print(u'   節內行：%d..%d（%d 行）' % (h + 1, nxt, nxt - h))
    for k in range(max(h, nxt - 26), nxt):
        print(u'   L%d| %s' % (k + 1, LINES[k][:170]))

# 四・第八章：即刻・解任・代表權・搜查・票
i8 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第八章'))
for w in (u'即刻', u'解任', u'代表人', u'搜', u'票'):
    for i, l in enumerate(LINES):
        if i >= i8 and w in l:
            print(u'== [%s] L%d| %s' % (w, i + 1, l[:300]))

# 五・附錄六各補遺之出處行
i6 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄六'))
cur = None
for i in range(i6, len(LINES)):
    l = LINES[i]
    if l.startswith(u'### 〔補遺'):
        cur = l[:44]
    if cur and (u'出處' in l or u'《四分律》' in l):
        print(u'== %s -> L%d| %s' % (cur, i + 1, l[:190]))
        cur = None

# 六・壇經偈之上下文
for i, l in enumerate(LINES):
    if u'壇經' in l:
        print(u'== 壇經 L%d| %s' % (i + 1, l[:230]))
