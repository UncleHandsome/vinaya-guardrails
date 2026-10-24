# -*- coding: utf-8 -*-
"""量而不刀：求某引文在本地語料之落檔，及前後最近之『卷N』錨（定卷之用）。"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, u'_work'))
import _tk                                                     # noqa: E402
import v39align                                                # noqa: E402

CN = u'〇一二三四五六七八九十百廿卌'
VOLRE = re.compile(u'卷第?([%s]{1,5})' % CN)


def num(s):
    v = _tk.cn_num(re.sub(u'^第', u'', s.strip()))
    return v if v else None


def locate(seg):
    out = []
    for fn, raw, nt, nm in v39align.CORPUS:
        p = nt.find(seg)
        while p >= 0:
            mp = nm[p]
            before = [(num(v), raw[max(0, mp - 3000):mp].rfind(u'卷第' + v) if v else -1)
                      for _m, v in [(m, m.group(1)) for m in VOLRE.finditer(raw[max(0, mp - 3000):mp])]]
            tail = raw[mp:mp + 20000]
            after = [num(m.group(1)) for m in VOLRE.finditer(tail)][:2]
            out.append((fn, [a[0] for a in before][-2:], after, mp, raw[mp - 60:mp + 60]))
            p = nt.find(seg, p + 1)
    return out


for seg in [u'若比丘如法諍事滅已後更發起者得波逸提',
            u'此某甲比丘犯僧殘罪不覆藏今從僧乞六夜摩那埵',
            u'若舉離本處初離處波羅夷',
            u'若取離處尼薩耆取而不離處突吉羅']:
    n = _tk.norm(seg)
    hits = locate(n)
    print(u'=== %s｜norm %d 字・落 %d 處' % (seg[:20], len(n), len(hits)))
    for fn, b, a, mp, ctx in hits:
        print(u'   %-16s 前卷%s 後卷%s @%d' % (fn, b, a, mp))
        print(u'      文：%s' % ctx.replace(u'\n', u''))
