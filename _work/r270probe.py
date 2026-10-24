# -*- coding: utf-8 -*-
"""270 輪・量一：自查 269 新寫之凡例第六節一句——『凡用之處須自註分界』今冊守得幾何。

法源：第 16・20 度之誡（驗器所排除之處即病所住）＋『立約須當場自量全書』：
      本輪所立之約，本輪先量自己守不守，不守則**改約以從實**或**補註以從約**，二者必居其一。
口徑：① 以凡例自舉之詞為鑰（證據能力・管轄・迴避），不自行擴詞（擴則以義為單位，墮假陽性）；
      ② 落點按『節』（H3）聚之，並記該節之內有無分界自註之語
         （會通・非佛制・世俗法上・對位・詳見第八章・引橋・功能對位・不取世俗…）；
      ③ 前七章＝第一章～第七章（第八章為其本域，不在此約）。
用法：python -X utf8 _work/r270probe.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')

CH = re.compile(u'^# (第([一二三四五六七八])章)(?:（(.+?)）)?')
SEC = re.compile(u'^### (.+)')
KEY = [u'證據能力', u'管轄', u'迴避']
NOTE = [u'會通', u'非佛制', u'世俗法上', u'對位', u'詳見第八章', u'引橋', u'功能對位',
        u'屬世俗', u'世俗法律', u'接引', u'非律制', u'律無']

# 逐節聚段
segs = []
cur = None
for i, l in enumerate(L):
    m = CH.match(l)
    if m:
        cur = {u'ch': m.group(2), u't': u'（章界）', u'a': i, u'b': i}
        segs.append(cur)
        continue
    if l.startswith(u'# ') or l.startswith(u'## '):
        cur = {u'ch': u'他', u't': l[:22], u'a': i, u'b': i}
        segs.append(cur)
        continue
    s = SEC.match(l) if l.startswith(u'### ') else None
    if s:
        if cur:
            cur[u'b'] = i
        cur = {u'ch': (segs[-1][u'ch'] if segs else u'他'), u't': s.group(1)[:30],
               u'a': i, u'b': i}
        segs.append(cur)
        continue
    if cur:
        cur[u'b'] = i
for g in segs:
    g[u'txt'] = u'\n'.join(L[g[u'a']:g[u'b'] + 1])

print(u'節段 %d 個' % len(segs))
tot = {}
for k in KEY:
    tot[k] = sum(1 for g in segs if g[u'ch'] in u'一二三四五六七' and k in g[u'txt'])
print(u'前七章含鑰詞之節數：%s' % tot)
naked = 0
for g in segs:
    if g[u'ch'] not in u'一二三四五六七':
        continue
    ks = [k for k in KEY if k in g[u'txt']]
    if not ks:
        continue
    has = any(x in g[u'txt'] for x in NOTE)
    if not has:
        naked += 1
        print(u'  無注・第%s章｜%-28s｜鑰：%s' % (g[u'ch'], g[u't'], u'・'.join(ks)))
print(u'——— 前七章以鑰詞為骨之節共 %d 段，其中**無分界自註** %d 段' % (
    sum(1 for g in segs if g[u'ch'] in u'一二三四五六七' and any(k in g[u'txt'] for k in KEY)), naked))
