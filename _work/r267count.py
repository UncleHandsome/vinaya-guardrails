# -*- coding: utf-8 -*-
"""267 輪・量三（終檢之數）：冊態・卡數・圍欄・27 目今可判之處（含卷首新入者）。"""
import hashlib
import io
import os
import re
import sys

from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
raw = open(P, 'rb').read()
print(u'bytes %d｜SHA %s' % (len(raw), hashlib.sha256(raw).hexdigest()[:12]))
L = io.open(P, encoding=u'utf-8-sig').read().split(u'\n')
print(u'lines %d｜案例卡 %d｜補遺 %d｜圍欄段 %d' % (
    len(L),
    sum(1 for l in L if l.startswith(u'### 〔案例')),
    sum(1 for l in L if l.startswith(u'### 〔補遺')),
    sum(1 for l in L if l.startswith(u'```'))))
BODY0 = next(i for i, l in enumerate(L) if l.startswith(u'# 第一章'))
Toc0 = next(i for i, l in enumerate(L) if l.startswith(u'## 【全書開卷標準目錄】'))
TIT = {}
for l in L:
    m = re.match(u'^### 〔(案例|補遺) ([0-9]+)〕(.*)$', l)
    if m:
        TIT[(m.group(1), m.group(2))] = re.split(u'—|--|：', m.group(3))[0]
PU = re.compile(u'[\\s\u3000，、；：？！。\u2014\\-「」『』（）()〔〕\\[\\]·]')


def pl(s):
    return PU.sub(u'', s)


def lcs(a, b):
    return SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b)).size


tot = head = nohead = 0
for i, l in enumerate(L):
    if (Toc0 <= i < BODY0) or l.startswith(u'### '):
        continue
    for m in re.finditer(u'〔(案例|補遺) ?([0-9]+)〕([一-鿿]{3,14})', l):
        tot += 1
        if i < BODY0:
            head += 1
        key = (m.group(1), m.group(2).zfill(2))
        headt = TIT.get(key, u'')
        nm = pl(m.group(3))
        if headt and lcs(nm, pl(headt)) < 2:
            bo, bk = max((lcs(nm, pl(h)), k2) for k2, h in TIT.items() if k2 != key)
            if bo >= 5:
                nohead += 1
                print(u'  ✗ L%d %s' % (i + 1, m.group(0)[:40]))
print(u'27 目今可判 %d 處（卷首新入 %d 處）・報 %d 處' % (tot, head, nohead))
print(u'28 目：無號形制 %d 見（須 0）' % len(re.findall(u'〔(?:案例|補遺)·|〔(?:案例|補遺)〕', u'\n'.join(L))))
