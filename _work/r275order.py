# -*- coding: utf-8 -*-
"""275 輪・新目之先驅量：目錄條與書身之題，**依序向前匹配**能合幾何。

所以先量而不即立目：『不指空』只問此題存在，不問此題在此章・在此序（v1 之錯遂無尺）。
今以「序」為約，須先量清書身有多少合法之不同形（第八章作兩 H1・目錄只列一次之類），
否則新目一立即以假紅問罪——**放寬前先量基線**（269 之誡）。
用法：PYTHONIOENCODING=utf-8 python -X utf8 _work/r275order.py
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _tk                                                        # noqa: E402

L = _tk.MAIN_LINES
Toc0 = next((i for i, l in enumerate(L) if l.startswith(u'## 【全書開卷標準目錄】')), 0)
BODY0 = next(i for i, l in enumerate(L) if l.startswith(u'# 第一章'))


def key(s):
    s = re.sub(u'（.*?）', u'', s, flags=re.S)
    return re.sub(u'[《》「」『』〔〕【】（）·：:，,、／/\\s#*➔\\-—]', u'', s)[:14]


TOCITEM = re.compile(u'^\\s+\\*+\\s*(?:\\*\\*)?(第([一二三四五六七八九十]+)章|第([一二三四五六七八九十]+)節|閘門([一二三四五六]))')
items = []
for i in range(Toc0, BODY0):
    m = TOCITEM.match(L[i])
    if m:
        kind = u'章' if m.group(2) else u'節'
        items.append((i + 1, kind, key(L[i]), L[i].strip()[:52]))

HEADS = []
for i in range(BODY0, len(L)):
    l = L[i]
    if l.startswith(u'# '):
        m = re.match(u'^# 第([一二三四五六七八九十]+)章', l)
        if m:
            HEADS.append((i + 1, u'章', key(l), l[:44]))
    elif l.startswith(u'### ') and not l.startswith(u'### 〔'):
        m = re.match(u'^### (?:第([一二三四五六七八九十]+)節|閘門([一二三四五六]))', l)
        if m:
            HEADS.append((i + 1, u'節', key(l[4:]), l[:44]))

j = 0
unmatched = []
for ln, kind, k, txt in items:
    while j < len(HEADS) and not (HEADS[j][1] == kind and HEADS[j][2] == k):
        j += 1
    if j >= len(HEADS):
        unmatched.append((ln, kind, txt))
    else:
        j += 1
print(u'目錄之條 %d（章 %d・節 %d）・書身之題 %d' % (
    len(items), sum(1 for x in items if x[1] == u'章'), sum(1 for x in items if x[1] == u'節'), len(HEADS)))
print(u'依序向前匹配：合 %d・不合 %d' % (len(items) - len(unmatched), len(unmatched)))
for ln, kind, txt in unmatched:
    print(u'   ✗ L%-5d %s｜%s' % (ln, kind, txt))
# 書身有而目錄未列之題（只報不判——目錄之制為 H1〜H3 之擇要）
skipped = [h for h in HEADS if h[2] not in {x[2] for x in items}]
print(u'書身之題而未見於目錄：%d 條（如實報數，不作判）' % len(skipped))
for h in skipped[:8]:
    print(u'   · L%-5d %s｜%s' % (h[0], h[1], h[3]))
