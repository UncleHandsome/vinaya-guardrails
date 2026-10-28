# -*- coding: utf-8 -*-
"""292・落點量（七大刀口之實數：次碼・深描・出堂洗心・三環・J 案・四奪・102 宣稱）。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
T = io.open(SRC, 'rb').read().decode('utf-8').replace(u'\r\n', u'\n')
L = T.split(u'\n')
PAGES = [i for i, x in enumerate(L) if x.startswith(u'<!--PAGE-->')]


def zone(i):
    if i < 60:
        return u'卷首'
    heads = [(k, x) for k, x in enumerate(L) if re.match(u'^# 第[一二三四五六七八九十]+章', x)]
    for n, (k, x) in enumerate(heads):
        nxt = heads[n + 1][0] if n + 1 < len(heads) else len(L)
        if k <= i < nxt:
            return x[:12]
    return u'其他'


def cnt(pat, label, show=0):
    rx = re.compile(pat) if not isinstance(pat, type(re.compile(u''))) else pat
    hits = [(i + 1, zone(i)) for i, x in enumerate(L) if rx.search(x)]
    n = sum(len(rx.findall(L[i - 1])) for i, _z in hits)
    from collections import Counter
    print(u'%-26s 見 %4d｜行 %4d｜%s' % (label, n, len(hits),
                                         dict(Counter(z for _i, z in hits))))
    if show:
        for i, z in hits[:show]:
            print(u'    L%-5d %s｜%s' % (i, z, L[i - 1][:110]))
    return hits


print(u'冊：%d 行' % len(L))
cnt(u'/ 遮\\d+', u'次碼 / 遮NN')
cnt(u'/ 僧\\d+', u'次碼 / 僧NN')
cnt(u'/ 開\\d+', u'次碼 / 開NN')
cnt(u'〔案例 \\d+ ?/ ', u'行內含次碼之案例號', 4)
cnt(u'深描', u'深描（全書）')
cnt(u'〔調部深描 ?\\d+〕', u'深描方括號式', 6)
cnt(u'出堂洗心', u'出堂洗心', 8)
cnt(u'洗心三事', u'洗心三事', 8)
cnt(u'三環', u'三環', 0)
cnt(u'夜半四照', u'夜半四照', 0)
cnt(u'三鏡', u'三鏡', 0)
cnt(u'隨身三印', u'隨身三印', 3)
cnt(u'J-[1-4]', u'J 碼', 0)
cnt(u'現代深水案例', u'現代深水案例', 0)
cnt(u'臨濟四奪|四奪', u'四奪', 0)
cnt(u'除偏鏡', u'除偏鏡', 6)
cnt(u'102', u'102 字樣', 0)
cnt(u'一百零二|百則', u'百則／一百零二', 0)
cnt(u'\\d+ 案', u'N 案', 0)
