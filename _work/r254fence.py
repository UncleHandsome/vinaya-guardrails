# -*- coding: utf-8 -*-
# ASCII-only patcher: 99 -> 102 inside the box line of the fence diagram,
# taking one cell back from the trailing pad so the width and the bar columns stay put.
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob
hits = [q for q in glob.glob(os.path.join(ROOT, 'ver39*.md')) if '\u5217\u5370' not in os.path.basename(q)]
assert len(hits) == 1, hits
p = hits[0]


def cw(s):
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


lines = io.open(p, encoding='utf-8').read().split('\n')
tgt = [i for i, l in enumerate(lines) if '99 \u7247' in l and '\u2502' in l]
assert len(tgt) == 1, tgt
i = tgt[0]
l0 = lines[i]
w0 = cw(l0)
bars0 = [k for k, c in enumerate(l0) if c in '\u2502\u251c\u2524']
l1 = l0.replace('99 片', '102 片')
b = l1.index('│')            # take the cell from the pad right after the box's left bar
jj = b + 1
while jj < len(l1) and l1[jj] == ' ':
    jj += 1
assert jj > b + 1, 'no inner pad'
l2 = l1[:b + 1] + l1[b + 2:]        # drop exactly one space there
assert cw(l2) == w0, (cw(l2), w0)
bars2 = [k for k, c in enumerate(l2) if c in '\u2502\u251c\u2524']
print('width %d -> %d | bar cols %s -> %s' % (w0, cw(l2), bars0, bars2))
assert bars2 == bars0, 'bar column moved'
lines[i] = l2
io.open(p, 'w', encoding='utf-8').write('\n'.join(lines))
print('fence line ok:', l2[:60])
