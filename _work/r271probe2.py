# -*- coding: utf-8 -*-
"""271 輪・量二（改口徑）：① 犍度名須**折異體**（冊作『犍度』、語料作『揵度』，不折則全成偽缺失）；
   ② 附錄級指針之子靶放寬為『附錄N＋（至多三字）＋『「【（』內之名』，並連『附錄N之第M目／款』同判。

用法：python -X utf8 _work/r271probe2.py
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
B = u'\n'.join(L)
PU = re.compile(u'[\\s\\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·／/]')


def norm(s):
    return PU.sub(u'', s)


NC = norm(_tk.VINAYA).replace(u'揵度', u'犍度')      # 折異體：語料之『揵』從册之『犍』
NB = norm(B)

print(u'── ① 犍度名（折異體後對語料）──')
forms = {}
for m in re.finditer(u'[一-鿿]{1,6}犍度', B):
    forms[m.group(0)] = forms.get(m.group(0), 0) + 1
bad = 0
for k in sorted(forms, key=lambda x: -forms[x]):
    nk = norm(k).replace(u'揵度', u'犍度')
    c = NC.count(nk)
    if not c:
        bad += 1
    print(u'  %-14s 全書 %-3d・語料 %d %s' % (k, forms[k], c, u'' if c else u'⚠ 語料無此連綴'))
print(u'  共 %d 形・語料無此連綴者 %d' % (len(forms), bad))

print(u'\n── ② 附錄級指針之子靶 ──')
APX = {}
order = []
for i, l in enumerate(L):
    m = re.match(u'^# (附錄[一二三四五六])', l)
    if m:
        APX[m.group(1)] = [i, len(L)]
        order.append(m.group(1))
for x in range(len(order) - 1):
    APX[order[x]][1] = APX[order[x + 1]][0]
BODY = {k: norm(u'\n'.join(L[APX[k][0]:APX[k][1]])) for k in APX}
PTR = re.compile(u'(附錄[一二三四五六])(?:之)?[^\\n「『【（。；]{0,3}[「『【（]([^」』））。\n]{2,26})[」』）】）]')
hit = 0
for i, l in enumerate(L):
    for m in PTR.finditer(l):
        a, sub = m.group(1), m.group(2).strip()
        n = norm(sub)
        if len(n) < 4 or not re.match(u'^[一-鿿]', n):
            continue
        if a not in APX:
            continue
        hit += 1
        wins = [n[k:k + 4] for k in range(max(1, len(n) - 3))]
        own = sum(1 for w in wins if w in BODY[a])
        other = [(sum(1 for w in wins if w in v), k) for k, v in BODY.items() if k != a]
        bn, bk = max(other) if other else (0, u'—')
        flag = u'中' if own else (u'靶外➔%s' % bk if bn >= 2 else u'未證')
        if flag != u'中':
            print(u'  %-4s L%-5d 子靶『%s』own=%d best=%d ➔ %s｜%s'
                  % (a, i + 1, sub[:20], own, bn, flag, l.strip()[:58]))
print(u'  小計：可判 %d 处（未列者即『中』）' % hit)
