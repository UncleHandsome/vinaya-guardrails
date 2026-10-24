# -*- coding: utf-8 -*-
"""282・量（四）：第七章之節題與心所軸・第八章之解任與搜查・附錄三四角之角色・編目公約・附錄六之調部標名。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)

H = re.compile(u'^(#{1,6}) +(.*)$')


def rng(mark):
    a = next((i for i, l in enumerate(LINES) if l.startswith(u'# ') and mark in l), None)
    b = next((i for i in range(a + 1, len(LINES)) if LINES[i].startswith(u'# ')), len(LINES))
    return a, b


# 甲・第七章
a, b = rng(u'第七章')
print(u'== 第七章 L%d..%d' % (a + 1, b + 1))
for i in range(a, b):
    m = H.match(LINES[i])
    if m and len(m.group(1)) <= 3:
        print(u'  L%d %s' % (i + 1, LINES[i][:60]))
print(u'  含『心所軸』之行：%s' % [i + 1 for i in range(a, b) if u'心所軸' in LINES[i]])
for n in (39, 67, 100):
    for i in range(a, b):
        if re.search(u'案例 0*%d(?:[^0-9]|〕)' % n, LINES[i]):
            print(u'  [案%d] L%d| %s' % (n, i + 1, LINES[i][:220]))

# 乙・第八章之去職與搜查
a8, b8 = rng(u'第八章')
for w in (u'解任', u'解職', u'停職', u'除名', u'喪失', u'職務', u'辭任', u'免職', u'登記', u'備查', u'搜查', u'搜索', u'隱私', u'票'):
    hs = [i + 1 for i in range(a8, b8) if w in LINES[i]]
    print(u'  八章[%s]：%d %s' % (w, len(hs), hs[:10]))
print(u'  全書[搜]：%d %s' % (T.count(u'搜'), [i + 1 for i, l in enumerate(LINES) if u'搜' in l][:22]))
for i in [6843, 6844, 6845, 6907, 6908, 6909, 6910, 6911, 7047, 7048]:
    print(u'  L%d| %s' % (i, LINES[i - 1][:300]))

# 丙・全書各章之『搜』
for i, l in enumerate(LINES):
    if u'搜' in l:
        print(u'  [搜] L%d| %s' % (i + 1, l[:150]))

# 丁・附錄三四角：全書用法
for who in (u'檀尼迦', u'沓婆摩羅子', u'慈地', u'象力'):
    hs = [i + 1 for i, l in enumerate(LINES) if who in l]
    print(u'  %s：%d 處 %s' % (who, len(hs), hs[:12]))
    for i in hs[:4]:
        print(u'      L%d| %s' % (i, LINES[i - 1][:150]))

# 戊・編目公約之現文
print(u'  『定義載體』：%d 處' % T.count(u'定義載體'))
for i, l in enumerate(LINES):
    if u'定義載體' in l:
        print(u'  L%d| %s' % (i + 1, l[:200]))

# 己・附錄六『調部文獻定位』之非調部者
i6, _ = rng(u'附錄六')
cur = None
for i in range(i6, len(LINES)):
    l = LINES[i]
    if l.startswith(u'### 〔補遺'):
        cur = l[:40]
    if u'調部文獻定位' in l:
        vol = re.findall(u'卷([一二三四五六七八九十百]+)', l)
        print(u'  %s｜卷%s' % (cur, vol))
