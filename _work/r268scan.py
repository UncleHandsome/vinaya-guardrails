# -*- coding: utf-8 -*-
"""268 輪・帳檢：記錄檔之簡形掃描，**排除「」／『』／反引號之例示**（供狀不動，只報敘事用字）。

用法：python -X utf8 _work/r268scan.py            # 只報
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import _simpmap
import _simpdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = set(_simpmap.S) | set(_simpdict.MAP.keys()) | set(u'两当强随旧总续证')
SKIP = re.compile(u'「[^」]*」|『[^』]*』|`[^`]*`')

for f in (u'列印SOP.md', os.path.join(u'_archive', u'編年工程日誌.md'), u'_work/v39secref.py',
          u'_work/r268neg.py', u'_work/r268sop.py', u'_work/r267sec.py', u'_work/r268net.py',
          u'_work/v39battery.py', u'_work/r267count.py'):
    p = os.path.join(ROOT, f)
    if not os.path.exists(p):
        print(u'（無此檔）%s' % f)
        continue
    bad = []
    for i, l in enumerate(io.open(p, encoding=u'utf-8-sig').read().split(u'\n')):
        seg = SKIP.sub(u'', l)
        for c in sorted(set(x for x in seg if x in K)):
            q = seg.find(c)
            bad.append((i + 1, c, seg[max(0, q - 14):q + 8]))
    print(u'%-30s 敘事區簡形 %d' % (f.split('/')[-1], len(bad)))
    for n, c, s in bad[:10]:
        print(u'      L%-5d %s  %r' % (n, c, s))
