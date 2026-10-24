# -*- coding: utf-8 -*-
"""283・補刀＋量：
① 凡例『一見』之數目宣稱改為可定位之表述（數不在尺內即不報）；
② 量全書跨章之長段重複（40 字之規窗），視其可否立為第 35 目。"""
import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
APPLY = u'--apply' in sys.argv
T = io.open(BOOK, encoding=u'utf-8-sig').read()
sha = lambda x: hashlib.sha256(x.encode(u'utf-8')).hexdigest()[:12]
print(u'正本 %d 行・sha %s' % (len(T.split(u'\n')), sha(T)))

OLD = (u'冊中遇其樞紐處自註分界，今有此類自註一見，**在第四章**（第三節之末云：'
       u'『屬證據能力之會通；其道場層面之調查標準作業與數位資產治理，詳見第八章第二節與第四節』），遇此類處皆作如是觀。')
NEW = (u'冊中遇其樞紐處自註分界，其標作〔編者自註・法域分界〕，今見於第四章第三節之末，其文云：'
       u'『屬證據能力之會通；其道場層面之調查標準作業與數位資產治理，詳見第八章第二節與第四節』——遇此類處皆作如是觀。')
print(u'①命中：%d' % T.count(OLD))
assert T.count(OLD) == 1
T = T.replace(OLD, NEW, 1)

L = T.split(u'\n')
H = re.compile(u'^#{1,6} +')
BODY0 = next(i for i, l in enumerate(L) if l.startswith(u'# 第一章'))
END = next(i for i, l in enumerate(L) if l.startswith(u'# 終卷'))
ch, cur = {}, u'?'
for i in range(BODY0, len(L)):
    if L[i].startswith(u'# '):
        cur = L[i][2:8]
    ch[i] = cur
print(u'② 章屬自 L%d 至 L%d（印面除卷首與終卷後）' % (BODY0 + 1, END + 1))

K = 40
sh = {}
for i in range(BODY0, END):
    l = L[i]
    if not l.strip() or l.strip().startswith((u'|', u'>', u'`')):
        continue
    n = re.sub(u'[^\\u4e00-\\u9fff]', u'', l)
    for j in range(0, max(0, len(n) - K + 1)):
        sh.setdefault(n[j:j + K], set()).add(i)
dup = {k: v for k, v in sh.items() if len({ch[i] for i in v}) > 1}
lines = sorted({i for v in dup.values() for i in v})
print(u'   跨章共串（≥%d 字之規）：%d 條・涉及 %d 行' % (K, len(dup), len(lines)))
for i in lines[:12]:
    print(u'      L%d@%s| %s' % (i + 1, ch[i], L[i][:90]))

print(u'改後 %d 行・sha %s' % (len(T.split(u'\n')), sha(T)))
if not APPLY:
    print(u'（乾跑・未落盤）')
    sys.exit(0)
io.open(BOOK, 'w', encoding=u'utf-8').write(T)
back = io.open(BOOK, encoding=u'utf-8-sig').read()
print(u'落盤訖・同=%s・sha %s' % (back == T, sha(back)))
