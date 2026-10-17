# -*- coding: utf-8 -*-
"""第七十二輪軸四（修正版）：附錄I-3 之『正理X』行 ↔『全書 N 則』宣稱，與第七章總表正理對位欄復算。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import _tk  # noqa

L = _tk.LINES
s7, e7 = _tk.sec(u'\u7b2c\u4e03\u7ae0')
hdr, ncol, rows = None, 0, {}
for i in range(s7, e7):
    l = L[i]
    if l.startswith('| \u7de8\u865f |'):
        cells = [x.strip() for x in l.split('|')]
        if u'\u6b63\u7406\u5c0d\u4f4d' in cells:
            hdr = {n: k for k, n in enumerate(cells)}
            ncol = len(cells)
        continue
    m = re.match(u'^\\|\\s*\u3014(\u906e|\u958b|\u50e7)(\\d+)\u3015\\s*\\|', l)
    if m and hdr:
        c = [x.strip() for x in l.split('|')]
        if len(c) == ncol:
            rows[(m.group(1), int(m.group(2)))] = c[hdr[u'\u6b63\u7406\u5c0d\u4f4d']]

CNT = {}
for n in range(1, 9):
    key = u'\u6b63\u7406' + u'\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b'[n - 1]
    CNT[key] = [k for k, v in rows.items() if key in v]

out = [u'=== 第七章總表正理對位復算（案例 %d 則）===' % len(rows)]
for k, v in CNT.items():
    out.append(u'  %s：%d 案' % (k, len(v)))
out.append('')
out.append(u'=== 附錄I-3 逐行宣稱 ↔ 復算 ===')
i3 = next(i for i, l in enumerate(L) if u'\u6838\u5fc3\u547d\u984c\u9328\u5b9a\u7d22\u5f15' in l and l.startswith('####'))
diff = 0
for j in range(i3, min(i3 + 60, len(L))):
    l = L[j]
    if not l.startswith('|'):
        continue
    mk = re.search(u'\u6b63\u7406[\u4e00\u4e8c\u4e94\u4e09\u516d\u56db\u4e03\u516b]', l[:70])
    mn = re.search(u'\u5168\u66f8\\s*(\\d{1,3})\\s*\u5247', l)
    if mk and mn:
        key, num = mk.group(0), int(mn.group(1))
        act = len(CNT.get(key, []))
        tag = u'\u76f8\u5408' if act == num else u'\u4e0d\u7b26 \u25c0'
        if act != num:
            diff += 1
        out.append(u'  L%-6d %s \u8f09 %3d \u5fa9\u7b97 %3d  %s' % (j + 1, key, num, act, tag))
out.append(u'  \uff08\u4e0d\u7b26 %d \u884c\uff09' % diff)
open(os.path.join(HERE, 'zhengli72.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('cases', len(rows), 'diff', diff)
