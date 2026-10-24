# -*- coding: utf-8 -*-
"""270 輪・量四：『蒙上省寫』之節級指針——第 10 目之網外一形。

現尺：第 10 目以『第N章第M節』為鑰，故『第八章第二節**與第四節**』之後一節全在網外
      （蒙上省『第八章』三字，是中文常形，不是缺陷；但它所指之節存否，應有人守）。
口徑：① 先以『第N章第M節』定其章，取其後同一句內以『、／與／及／或』相連之『第K節』；
      ② 判 K 是否見於該章之節名集合（第三章以閘門為節，故其『第K節』若無從歸，如實報『節制不合』）；
      ③ 只報不擋者：K 前另有他章名者（已另有所屬）。
用法：python -X utf8 _work/r270ellip.py
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = [q for q in os.listdir(ROOT) if q.startswith(u'ver39') and q.endswith(u'.md')
        and u'列印' not in q][0]
L = io.open(os.path.join(ROOT, NAME), encoding=u'utf-8-sig').read().split(u'\n')
FULL = u'\n'.join(L)
CN = u'一二三四五六七八九十'
secs = {}                                       # 章 -> 節序集合
cur = None
for l in L:
    m = re.match(u'^# 第([' + CN + u']+)章', l)
    if m:
        cur = u'第%s章' % m.group(1)
        secs.setdefault(cur, set())
        continue
    if l.startswith(u'# '):
        cur = None
        continue
    if cur:
        s = re.match(u'^### 第([' + CN + u']+)節', l)
        if s:
            secs[cur].add(s.group(1))
        g = re.match(u'^### 閘門([' + CN + u'])', l)
        if g:
            secs[cur].add(g.group(1))
print(u'章 %d・節數 %s' % (len(secs), {k: len(v) for k, v in sorted(secs.items())}))

HEAD = re.compile(u'第([' + CN + u']+)章第([' + CN + u']+)節')
TAIL = re.compile(u'[、與及或（）\\s]{0,3}第([' + CN + u']+)節')
hit = miss = 0
for i, l in enumerate(L):
    for m in HEAD.finditer(l):
        ch = u'第%s章' % m.group(1)
        # 同一句內（至下一個句號）之蒙上省寫
        seg = l[m.end():l.find(u'。') if u'。' in l[m.end():] else len(l)]
        for t in TAIL.finditer(seg):
            k = t.group(1)
            if re.search(u'第[' + CN + u']+章', seg[:t.start()]):
                continue                          # 另有所屬
            hit += 1
            if ch not in secs:
                print(u'  L%-5d 章不可求：%s' % (i + 1, ch))
                miss += 1
            elif k not in secs[ch]:
                miss += 1
                print(u'  L%-5d 省寫落空｜%s 無第%s節｜今有：%s｜%s'
                      % (i + 1, ch, k, u'・'.join(sorted(secs[ch])), l.strip()[:92]))
print(u'——— 蒙上省寫之節級指針 %d 处・落空 %d' % (hit, miss))
