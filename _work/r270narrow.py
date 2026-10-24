# -*- coding: utf-8 -*-
"""270 輪・量二：窄口徑——前七章之內，何節真以『世俗實定法之具體制度』為骨（非僅借通用法理語）。

口徑：鑰詞取**實定法之專名**（公訴・檢調・強制通報・時效・法人・信託・稅・勞動・薪資・保險・
      法院・起訴・判決・強制報告・個資・監視器・銀行），而非『管轄／迴避』这类通用法理語（後者為全書公堂喻之骨架）。
用法：python -X utf8 _work/r270narrow.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
CH = re.compile(u'^# 第([一二三四五六七八])章')
SEC = re.compile(u'^### (.+)')
POS = [u'公訴', u'檢調', u'強制通報', u'時效', u'法人', u'信託', u'稅', u'勞動', u'薪資',
       u'保險', u'法院', u'起訴', u'判決', u'個資', u'監視', u'銀行', u'警', u'檢察']
NOTE = [u'會通', u'非佛制', u'世俗法上', u'對位', u'詳見第八章', u'引橋', u'功能對位',
        u'屬世俗', u'接引', u'非律制', u'低標', u'不共', u'界内不']

segs = []
cur = None
for i, l in enumerate(L):
    m = CH.match(l)
    if m or l.startswith(u'# ') or l.startswith(u'## '):
        if l.startswith(u'# '):
            mm = CH.match(l)
            cur = {u'ch': mm.group(1) if mm else u'他', u't': l[2:26], u'a': i, u'b': i}
            segs.append(cur)
        else:
            if cur:
                cur[u'b'] = i - 1
            cur = None
        continue
    s = SEC.match(l) if l.startswith(u'### ') else None
    if s:
        if cur:
            cur[u'b'] = i - 1
        ch = segs[-1][u'ch'] if segs else u'他'
        cur = {u'ch': ch, u't': s.group(1)[:30], u'a': i, u'b': i}
        segs.append(cur)
        continue
    if cur:
        cur[u'b'] = i
for g in segs:
    g[u'txt'] = u'\n'.join(L[g[u'a']:g[u'b'] + 1])

hit = 0
for g in segs:
    if g[u'ch'] not in u'一二三四五六七':
        continue
    ks = [k for k in POS if k in g[u'txt']]
    if not ks:
        continue
    hit += 1
    has = [x for x in NOTE if x in g[u'txt']]
    n = sum(g[u'txt'].count(k) for k in ks)
    print(u'%s｜第%s章｜%-30s｜鑰 %2d：%s%s' % (
        u'有注' if has else u'無注', g[u'ch'], g[u't'], n, u'・'.join(ks[:7]),
        u'　←注：%s' % u'・'.join(has[:3]) if has else u''))
print(u'——— 前七章含實定法專名之節：%d 段' % hit)
print(u'（對照）第八章同口徑：')
for g in segs:
    if g[u'ch'] != u'八':
        continue
    ks = [k for k in POS if k in g[u'txt']]
    if ks:
        print(u'    %-32s 鑰 %d' % (g[u't'][:30], sum(g[u'txt'].count(k) for k in ks)))
