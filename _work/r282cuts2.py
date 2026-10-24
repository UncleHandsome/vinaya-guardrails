# -*- coding: utf-8 -*-
"""282・補刀：導言界說去其自報之『七則』數（此數不在任何尺內，改以實名之卷段代之）；
   並覆量：第八章第二節之『四項』今列幾項、附錄六十五則之非調部引卷有幾則、附錄三人名表今幾行。"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
BAK = os.path.join(ROOT, u'_work', u'ver39.pre282b.md')
APPLY = u'--apply' in sys.argv
T = io.open(BOOK, encoding=u'utf-8-sig').read()
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]
print(u'正本 %d 行・sha %s' % (len(T.split(u'\n')), sha(T)))

OLD = u'本編十五則以調部（卷五十五至五十七）為體，其七則之判例母型兼引犍度部'
NEW = u'本編十五則以調部（卷五十五至五十七）為體，其判例母型復兼引犍度部'
assert T.count(OLD) == 1, T.count(OLD)
T2 = T.replace(OLD, NEW, 1)
print(u'刀：界說去自報之數')

# 覆量一・第八章第二節之編號項
L = T2.split(u'\n')
h = next(i for i, l in enumerate(L) if l.startswith(u'#### 二、創傷知情面談'))
n = next(i for i in range(h + 1, len(L)) if L[i].startswith(u'#### '))
items = [L[i][:70] for i in range(h, n) if re.match(u'^\\d+\\.  ', L[i])]
print(u'［量］第二節・創傷知情面談之編號項：%d 項' % len(items))
for it in items:
    print(u'   %s' % it)
said = [L[i][:90] for i in range(h, n) if u'項剛性操作標準' in L[i]]
print(u'［量］自稱之句：%s' % said)

# 覆量二・附錄六十五則之非調部引卷
i6 = next(i for i, l in enumerate(L) if l.startswith(u'# 附錄六'))
cards = []
cur = None
for i in range(i6, len(L)):
    if L[i].startswith(u'### 〔補遺'):
        cur = L[i][:34]
    if cur and u'原典文獻定位' in L[i]:
        cards.append((cur, L[i]))
        cur = None
non = [(c, ln) for c, ln in cards if re.search(u'卷(三十八|四十四|四十五|一|二|三|四)(?:[^〇-龥]|$)', ln)]
print(u'［量］定位欄：%d 則・其中引非調部之卷者 %d 則' % (len(cards), len(non)))
for c, ln in non:
    print(u'   %s' % c)

# 覆量三・附錄三人名表之行數
a3 = next(i for i, l in enumerate(L) if l.startswith(u'### 二、律典原生人名'))
b3 = next(i for i in range(a3 + 1, len(L)) if L[i].startswith(u'#'))
rows = [i for i in range(a3, b3) if L[i].lstrip().startswith(u'| **')]
print(u'［量］人名表人物行：%d 行（尾三：%s）' % (len(rows), [L[i][:34] for i in rows[-3:]]))
for i in rows[-4:]:
    print(u'   L%d| %s' % (i + 1, L[i][:190]))

print(u'改後 %d 行・sha %s' % (len(T2.split(u'\n')), sha(T2)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
if not os.path.exists(BAK):
    io.open(BAK, 'w', encoding=u'utf-8').write(T)
io.open(BOOK, 'w', encoding=u'utf-8').write(T2)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・同=%s・sha %s' % (back == T2, sha(back)))
