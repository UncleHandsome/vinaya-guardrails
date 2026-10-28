# -*- coding: utf-8 -*-
r"""289・報告『逐條核驗無誤清單』之本律九條復核（唯讀）。

法：去標點求片段於 _tk.VINAYA，並定位其所在分段檔；再取本冊引卷號與檔段比對（檔級粒度）。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import v39align as VA                                    # noqa: E402
import _tk                                               # noqa: E402

V = _tk.VINAYA
CORP = [(n, t) for n, r, t, i in VA.CORPUS]
RANGE = {u'01-10原文.txt': (1, 10), u'11-21 原文.txt': (11, 21), u'22-30 原文.txt': (22, 30),
         u'31-37 原文.txt': (31, 37), u'38-49 原文.txt': (38, 49), u'50-60 原文.txt': (50, 60)}
CN = u'〇一二三四五六七八九十'


def c2n(s):
    if u'十' in s:
        a, _, b = s.partition(u'十')
        return (CN.index(a) if a else 1) * 10 + (CN.index(b) if b else 0)
    return CN.index(s)


ITEMS = [
    (u'卷一・十句義', u'與諸比丘結戒集十句義', 1),
    (u'卷一・攝取於僧', u'攝取於僧', 1),
    (u'卷五十七・一義制呵責', u'如來出世以一義故為諸比丘制呵責羯磨', 57),
    (u'卷五十七・二義制斷諍', u'世尊以二義制斷諍法', 57),
    (u'卷三十二・伊羅鉢羅', u'我念古昔迦葉佛時', 32),
    (u'卷四十八・曾出嫡', u'曾出嫡', 48),
    (u'卷四十七・象力', u'此象力釋子好論議', 47),
    (u'卷四十八・草覆地', u'云何草覆地', 48),
    (u'卷五十八・三法不受大戒', u'有三法不應與受大戒', 58),
    (u'卷五十八・四法知可懺', u'知可懺罪', 58),
]
ok = miss = incon = 0
for tag, frag, juan in ITEMS:
    files = [n for n, t in CORP if frag in t]
    inV = V.count(frag)
    fit = [RANGE[n] for n in files if RANGE[n][0] <= juan <= RANGE[n][1]]
    if not files:
        miss += 1
        verdict = u'✘ 語料無此文'
    elif fit:
        ok += 1
        verdict = u'✔ 卷%d 落於檔段 %s' % (juan, u'・'.join(u'%d-%d' % f for f in fit))
    else:
        incon += 1
        verdict = u'△ 文在 %s，唯卷%d 不在其檔段' % (u','.join(files), juan)
    print(u'%-24s 語料 %d 見｜%s' % (tag, inV, verdict))
print(u'\n復核：合 %d・無文 %d・不相容 %d（共 %d 條）' % (ok, miss, incon, len(ITEMS)))

print(u'\n【本冊引卷與語料檔段之相符性（全書自動核）】——見 v39volchk 今量：核合 136／不合 0／未證 18')
