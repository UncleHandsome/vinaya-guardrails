# -*- coding: utf-8 -*-
"""第六十七輪探測二：指涉句與目標節題之 keyword 交集為零者（人工複核清單）。"""
import io
import re
from collections import defaultdict

import _tk as t

L = io.open(t.SRC, encoding='utf-8').read().split('\n')

CN = u'一二三四五六七八九十'
sec_of = defaultdict(dict)
cur = None
for i, l in enumerate(L):
    m = None
    if l.startswith('# '):
        mm = re.match(r'^# 第(.)章', l)
        cur = mm.group(1) if mm else None
    if cur and l.startswith('### '):
        m3 = re.match(r'^### 第(.)節', l)
        if m3:
            sec_of[cur][m3.group(1)] = l[4:]

STOP = set(u'第章節款目見詳参阅考之與及為於其此书本书中所有一二三二四五六七八九十０一'
           u' ' + u'，。、；：（）「」『』【】〔〕—‧' + u'0123456789')
pat = re.compile(u'第([%s])章第([%s])節' % (CN, CN))
out = []
zero = []
for i, l in enumerate(L):
    for m in pat.finditer(l):
        a, b = m.group(1), m.group(2)
        title = sec_of.get(a, {}).get(b)
        if title is None:
            zero.append((i + 1, a, b, l[:90], '節序不存在'))
            continue
        ctx = l[max(0, m.start() - 46):m.end() + 46]
        tw = set(c for c in title if c not in STOP)
        # 以二字詞比對，較穩
        twords = set()
        for k in range(len(title) - 1):
            w = title[k:k + 2]
            if all(c not in STOP for c in w):
                twords.add(w)
        hit = [w for w in twords if w in ctx]
        if len(hit) < 1:
            zero.append((i + 1, a, b, ctx, '無關鍵字重疊→' + title[:26]))
out.append('=== 疑義清單（無任何二字詞重疊／節序不存在）%d 筆 ===' % len(zero))
for n, a, b, ctx, why in zero:
    out.append('L%-6d 第%s章第%s節｜%s\n        %s' % (n, a, b, why, ctx))
io.open('_work/sweep67b.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(zero))
