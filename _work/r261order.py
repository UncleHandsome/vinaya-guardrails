# -*- coding: utf-8 -*-
"""261 輪・日誌正序器：260 條因錨點重複而落在 258 之前，本器按條號重排（只搬整塊，不動一字）。
斷言：條號序列須為 255…260 遞升；各塊首行以『N. **第』起，塊尾即下一條首行前之空行。
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, u'_archive', u'編年工程日誌.md')
APPLY = u'apply' in sys.argv
L = io.open(P, encoding=u'utf-8').read().split(u'\n')
START = re.compile(u'^(2\\d\\d)\\. \\*\\*第')
marks = [(int(m.group(1)), i) for i, l in enumerate(L) if (m := START.match(l))]
tail0 = min(i for n, i in marks if n >= 255)
head = L[:tail0]
blocks, pos = [], [(n, i) for n, i in marks if n >= 255]
for k, (n, i) in enumerate(pos):
    j = pos[k + 1][1] if k + 1 < len(pos) else len(L)
    blocks.append((n, L[i:j]))
nums = [n for n, _b in blocks]
print(u'今序：%s' % nums)
assert len(set(nums)) == len(nums), u'條號有重'
blocks.sort(key=lambda x: x[0])
out = head + [l for _n, b in blocks for l in b]
assert len(out) == len(L), u'搬移前後行數須同（%d≠%d）' % (len(out), len(L))
assert [int(m.group(1)) for m in
        re.finditer(u'(?m)^(2\\d\\d)\\. \\*\\*第', u'\n'.join(out))
        if int(m.group(1)) >= 255] == sorted(nums), u'重排後仍非遞升'
print(u'正序：%s' % sorted(nums))
if APPLY:
    io.open(P, 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(out))
    back = io.open(P, encoding=u'utf-8').read().split(u'\n')
    assert len(back) == len(L)
    print(u'———— 已正序落檔（%d 行不動）' % len(L))
else:
    print(u'———— 只報（apply 方改）')
