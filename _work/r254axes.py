# -*- coding: utf-8 -*-
"""第 254 輪・量尺四：第七章第二節四軸之缺案、重號與『共 N 案』失實之清點。"""
import io
import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = io.open(os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md'),
            encoding=u'utf-8').read().split(u'\n')
i7 = next(i for i, l in enumerate(L) if l.startswith(u'# 第七章'))
i8 = next(i for i, l in enumerate(L) if l.startswith(u'# 第八章'))
sec = L[i7:i8]
s2 = next(i for i, l in enumerate(sec) if l.startswith(u'### 第二節'))
s3 = next(i for i, l in enumerate(sec[s2 + 1:], s2 + 1) if l.startswith(u'### 第三節'))
ALL = set(range(1, 103))
axes = {}
cur = None
for i in range(s2, s3):
    l = sec[i]
    if l.startswith(u'#### '):
        cur = l[5:].strip()
        axes[cur] = []
    elif cur:
        axes[cur].append((i + s2 + 1, l))

for name, rows in axes.items():
    nums, dups, claimed = [], [], []
    for ln, l in rows:
        nums += [int(x) for x in re.findall(u'〔案例 ?(\\d{1,3})〕', l)]
        c = Counter([int(x) for x in re.findall(u'〔案例 ?(\\d{1,3})〕', l)])
        dups += [(ln, k, v) for k, v in c.items() if v > 1]
        claimed += re.findall(u'共 (\\d+) 案|(\\d+) 案）', l)
    miss = sorted(ALL - set(nums))
    print(u'==== %s' % name)
    print(u'   計入 %d 處｜不同案 %d｜缺 %d：%s' % (len(nums), len(set(nums)), len(miss), miss))
    if dups:
        print(u'   同行重號：%s' % dups[:8])
    cl = re.findall(u'共 (\\d+) 案', u'\n'.join(l for _n, l in rows)) + \
        re.findall(u'（(\\d+) 案', u'\n'.join(l for _n, l in rows))
    print(u'   自報案數：%s' % cl)

meta = [l for l in sec[s2:s3] if u'則判例' in l]
print(u'==== 節內之總數宣稱 ====')
for m in meta:
    print(u'   %.90s' % m.strip())
