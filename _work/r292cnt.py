# -*- coding: utf-8 -*-
"""292・帳前之量：印面行數・圍欄段數・三十二字詩偈之載體數。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
L = io.open(SRC, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n').split(u'\n')
FENCE = chr(0x60) * 3
op, n = None, 0
for i, x in enumerate(L):
    if x.strip().startswith(FENCE):
        if op is None:
            op = i
        else:
            n += 1
            op = None
print(u'行數 %d｜圍欄段 %d｜未閉之柵 %s' % (len(L), n, op is not None))
print(u'詩偈「善護三業，但自觀行」載體：%d' % sum(x.count(u'善護三業，但自觀行') for x in L))
print(u'「出堂洗心」今 %d 見｜「四境演繹判例」今 %d 見｜「調部專題」今 %d 見' % (
    sum(x.count(u'出堂洗心') for x in L), sum(x.count(u'四境演繹判例') for x in L),
    sum(x.count(u'調部專題') for x in L)))
