# -*- coding: utf-8 -*-
"""271 輪・量一：兩形並量——① 『附錄N＋子靶』之指針（子靶是否真見於該附錄）；
   ② 『X犍度』之篇名（是否見於本地語料、全書是否異形並用）。

法源：第十七度『每立一條 A→B 之檢，當場寫下它的反向 B→A 並問誰守著』之延伸——
      章・節・案例・行號・卷次俱有尺，**附錄內之子靶與犍度篇名**是最後兩處無尺之歸屬宣稱。
口徑：① 附錄級指針之形＝『附錄[一二三四五六]』之後同句內有『・Y』『之Y』『（Y）』『第M目／款／表』，
        子靶 Y 折標點取四字窗，數其見於**該附錄本文**者（他處見的不算，否則蒙錯附錄亦過）；
      ② 犍度名＝『([^\\s，。、；：「」『』（）〔〕]{1,6}犍度)』全書之形，逐一查語料（折標點後計見數）；
      ③ 判語只報不判，由人逐條裁。
用法：python -X utf8 _work/r271probe.py
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
CORP = _tk.VINAYA
PU = re.compile(u'[\\s\\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·／/]')


def norm(s):
    return PU.sub(u'', s)


NCORP = norm(CORP)

# ── 附錄界 ──
APX = {}
for i, l in enumerate(L):
    m = re.match(u'^# (附錄[一二三四五六])', l)
    if m:
        APX.setdefault(m.group(1), [i, len(L)])
    elif l.startswith(u'# ') and APX and m is None:
        pass
ks = sorted(APX, key=lambda k: APX[k][0])
for a, b in [(ks[x], ks[x + 1]) for x in range(len(ks) - 1)]:
    APX[a][1] = APX[b][0]
APX[ks[-1]][1] = len(L)
print(u'附錄 %d 篇：%s' % (len(ks), u'・'.join(u'%s(L%d-%d)' % (k, APX[k][0] + 1, APX[k][1]) for k in ks)))

PTR = re.compile(u'(附錄[一二三四五六])(?:・|之|（|\()([^（）。\n]{2,28})')
print(u'\n── ① 附錄級指針之子靶 ──')
hit = miss = 0
for i, l in enumerate(L):
    for m in PTR.finditer(l):
        a, sub = m.group(1), m.group(2).strip()
        sub = re.sub(u'[）]$', u'', sub)
        n = norm(sub)
        if len(n) < 4 or not re.match(u'^[一-鿿]', n):
            continue
        body = norm(u'\n'.join(L[APX[a][0]:APX[a][1]])) if a in APX else u''
        wins = [n[k:k + 4] for k in range(max(1, len(n) - 3))]
        own = sum(1 for w in wins if w in body)
        hit += 1
        if own == 0:
            miss += 1
            print(u'  靶外 L%-5d %s｜子靶『%s』・全書他處見：%s｜%s'
                  % (i + 1, a, sub[:22], u'有' if any(w in NCORP or norm(B) for w in wins) else u'無',
                     l.strip()[:64]))
print(u'  小計：可判 %d 处・子靶全不落該附錄者 %d' % (hit, miss))

print(u'\n── ② 犍度名之形與語料 ──')
forms = {}
for m in re.finditer(u'([一-鿿]{1,6}犍度)', B):
    forms.setdefault(m.group(1), []).append(L.index(m.group(0)[:12]) + 1 if False else 0)
for k in sorted(forms, key=lambda x: -len(forms[x])):
    nk = norm(k)
    print(u'  %-12s 全書 %-3d 見・語料 %d 見%s'
          % (k, B.count(k), NCORP.count(nk), u'' if NCORP.count(nk) else u'   ⚠ 語料無此形'))
