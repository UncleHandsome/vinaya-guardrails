# -*- coding: utf-8 -*-
"""271 輪・量三：① 五筆犍度疑點之上下文；② 以**寬式**複驗『附錄N＋名』之形（防網眼過小）。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')

print(u'── ① 五筆疑點之上下文 ──')
for k in [u'僧殘犍度', u'於藥犍度', u'結集等二十犍度', u'第四分雜犍度', u'二十犍度']:
    print(u'  【%s】' % k)
    n = 0
    for i, l in enumerate(L):
        p = l.find(k)
        while p >= 0:
            n += 1
            print(u'      L%-5d …%s…' % (i + 1, l[max(0, p - 34):p + len(k) + 24]))
            if n >= 2:
                break
            p = l.find(k, p + 1)
        if n >= 2:
            n = 0

print(u'\n── ② 寬式：凡『附錄N』後 14 字內之括號／引號內名 ──')
pat = re.compile(u'(附錄[一二三四五六])[^\\n]{0,14}?[（【「『]([^」』）】]{2,26})[」』）】]')
c = 0
for i, l in enumerate(L):
    for m in pat.finditer(l):
        c += 1
        print(u'   L%-5d %s｜%s｜%s' % (i + 1, m.group(1), m.group(2)[:24], l.strip()[:60]))
print(u'   合 %d 处' % c)
print(u'\n── ③ 『附錄N・』與『附錄N 之』式 ──')
for p, lab in [(re.compile(u'附錄[一二三四五六]・[^\\n，。；]{2,20}'), u'附錄N・X'),
               (re.compile(u'附錄[一二三四五六]之[一-鿿]{2,12}'), u'附錄N之X'),
               (re.compile(u'附錄[一二三四五六]（[^）]{2,20}）'), u'附錄N（X）')]:
    hits = [m.group(0) for m in p.finditer(u'\n'.join(L))]
    print(u'   %-9s %d 見：%s' % (lab, len(hits), u'｜'.join(sorted(set(hits))[:6])[:190]))
