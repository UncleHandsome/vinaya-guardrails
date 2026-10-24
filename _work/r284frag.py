# -*- coding: utf-8 -*-
"""284・器（小）：以 281 之回圖法自 `v39align.CORPUS`（帶標點之原始檔）取回逐字片段。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import v39align  # noqa: E402

FRAGS = [
    u'時世尊以無數方便呵責闡陀比丘已告諸比丘自今已去聽白已當名作餘語',
    u'云何僧與作不同住僧與作不見犯羯磨不懺悔羯磨惡見不捨羯磨是為僧與作不同住',
]


def raw_slice(pn, pad=0):
    for fn, raw, nt, nm in v39align.CORPUS:
        pos = nt.find(pn)
        if pos < 0:
            continue
        a = nm[pos]
        b = nm[pos + len(pn) - 1] + 1
        return fn, raw[max(0, a - pad):a], raw[a:b], raw[b:b + pad]
    return None, None, None, None


for f in FRAGS:
    g = re.sub(u'[^\\u4e00-\\u9fff]', u'', f)
    fn, pre, mid, post = raw_slice(g, 24)
    print(u'\n◆ 片段 %d 字・檔=%s' % (len(g), fn))
    if mid:
        print(u'  前：%s' % pre)
        print(u'  本：%s' % mid)
        print(u'  後：%s' % post)
        print(u'  覆核・歸一後與冊文同：%s' % (re.sub(u'[^\\u4e00-\\u9fff]', u'', mid) == g))
