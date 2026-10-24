# -*- coding: utf-8 -*-
"""274 輪・量④：換入後之盈虛——舊 ch1-3 獨有之行都掉了什麼、新稿補了什麼、名相有無後退。"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = [x for x in os.listdir(ROOT) if x.startswith(u'ver39') and x.endswith(u'.md')
     and u'\u5217\u5370' not in x][0]
NEW = io.open(os.path.join(ROOT, Q), encoding=u'utf-8-sig').read().split(u'\n')
OLD = io.open(os.path.join(ROOT, u'_work', 'r274swap.bak'), encoding=u'utf-8').read().split(u'\n')


def span(L):
    a = next(i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u4e00\u7ae0'))
    z = next(i for i, l in enumerate(L) if l.startswith(u'# \u7b2c\u56db\u7ae0'))
    return L[a:z]


o, n = span(OLD), span(NEW)
print(u'舊 ch1-3 %d 行｜新 ch1-3 %d 行' % (len(o), len(n)))
setn = set(l.strip() for l in n)
lost = [l.strip() for l in o if len(l.strip()) >= 25 and l.strip() not in setn]
print(u'\n壹・舊有而今無之長行：%d 行' % len(lost))
q1 = [l for l in lost if u'\u300c' in l]
q2 = [l for l in lost if l.startswith(u'#')]
q3 = [l for l in lost if l.startswith(u'|')]
print(u'   内含「」者 %d 行・標題行 %d 行・表列 %d 行' % (len(q1), len(q2), len(q3)))
print(u'   —— 掉落之標題：')
for l in q2[:14]:
    print(u'      %s' % l[:56])

T = u'\n'.join
for k in [u'\u51fa\u7f6a\u9084\u6de9\u56db\u4e8b', u'\u51fa\u9662\u5100\u8ecc', u'\u6cd5\u5b9a\u56db\u7f70',
          u'\u88c1\u6c7a\u767b\u9332\u65e5\u8a8c', u'\u5b58\u6a94\u5361', u'\u8b66\u7b56', u'\u7981\u7d04',
          u'\u4e94\u652f\u7269\u4e3b', u'\u4e8c\u89b0\u56db\u7580', u'\u63a8\u9032\u6642\u9593\u7dda',
          u'\u9053\u5c94', u'\u25c8', u'\u25ce', u'\u591c\u534a\u56db\u7167', u'\u4e09\u79d2\u5b9a\u97f3']:
    print(u'   %-8s 舊 %2d・新 %2d' % (k, T(o).count(k), T(n).count(k)))

gain = [l.strip() for l in n if len(l.strip()) >= 25 and l.strip() not in set(x.strip() for x in o)]
print(u'\n贰・新有而舊無之長行：%d 行（其首 12 例）' % len(gain))
for l in gain[:12]:
    print(u'      %s' % l[:60])
print(u'\n叁・指針之數：〔案例 舊 %d・新 %d｜〔補遺 舊 %d・新 %d' % (
    T(o).count(u'\u3014\u6848\u4f8b'), T(n).count(u'\u3014\u6848\u4f8b'),
    T(o).count(u'\u3014\u88dc\u907a'), T(n).count(u'\u3014\u88dc\u907a')))
print(u'    『第N章』式 舊 %d・新 %d' % (T(o).count(u'\u7b2c') , 0) if False else u'')
import re
print(u'    第N章第M節 舊 %d・新 %d' % (len(re.findall(u'\u7b2c.\u7ae0\u7b2c.\u7bc0', T(o))),
                                      len(re.findall(u'\u7b2c.\u7ae0\u7b2c.\u7bc0', T(n)))))
