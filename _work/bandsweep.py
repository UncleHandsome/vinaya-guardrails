# -*- coding: utf-8 -*-
"""以 50-60 檔之「調部之一～毘尼增一之四」分段標題為錨，覆核全書「卷五十X／毘尼增一之N ＋ L行號」之配對。"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT = _tk.ROOT
rows = [l.strip() for l in io.open(os.path.join(ROOT, u'原文', u'50-60 原文.txt'), encoding='utf-8-sig')]
marks = []
for i, l in enumerate(rows, 1):
    if len(l) < 28 and re.match(u'^(調部之|毘尼增一之)', l):
        marks.append((i, l))
BAND = {}
for k, (ln, name) in enumerate(marks):
    end = marks[k + 1][0] - 1 if k + 1 < len(marks) else len(rows)
    BAND[name] = (ln, end)
VOL = {u'調部之一': u'卷五十五', u'調部之二': u'卷五十六', u'調部之三': u'卷五十七',
       u'毘尼增一之一': u'卷五十八', u'毘尼增一之二': u'卷五十八～五十九',
       u'毘尼增一之三': u'卷五十九', u'毘尼增一之四': u'卷五十九～六十'}
out = [u'分段錨點：' + u'；'.join(u'%s=%s(%s)' % (n, BAND[n], VOL[n]) for n in BAND)]

LIN = re.compile(u'L\\s*(\\d{1,4})(?:\\s*[–—~-]\\s*(\\d{1,4}))?')
CLAIM = re.compile(u'(卷五十[五六七])')
NAME = {u'卷五十五': u'調部之一', u'卷五十六': u'調部之二', u'卷五十七': u'調部之三'}
L = _tk.LINES
bad = 0
for i, line in enumerate(L):
    cl = set(CLAIM.findall(line))
    nums = []
    for m in LIN.finditer(line):
        a = int(m.group(1))
        b = int(m.group(2)) or a if m.group(2) else a
        if not (100 <= a <= 2000):
            continue
        nums.extend([a, min(b, a + 30)])
    if not cl or not nums:
        continue
    for c in cl:
        band = BAND.get(NAME.get(c, c))
        if not band:
            continue
        lo, hi = band
        outnum = [n for n in nums if not (lo <= n <= hi)]
        if outnum and len(outnum) == len(nums):
            bad += 1
            out.append(u'FAIL L%d %s(%s) 而所列行號 %s :: %s' % (i + 1, c, band, nums, line[:120]))
        elif outnum:
            out.append(u'part L%d %s(%s) 越界行號 %s :: %s' % (i + 1, c, band, outnum, line[:100]))
out.insert(1, u'全數越界 %d 行' % bad)
io.open(os.path.join(ROOT, u'_work', u'band.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(bad, len(out))
