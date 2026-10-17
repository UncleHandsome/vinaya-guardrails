# -*- coding: utf-8 -*-
"""第七十二輪軸二：標題重出與錨點之可辨性（同名 H2／H3／H4 會使 pandoc 錨點加後綴、款級引用兩指）。"""
import io, os, re, sys
from collections import defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(ROOT, u'ver38四分律_起心動念心智分析框架_修正版.md'), encoding='utf-8').read()
LINES = DOC.split('\n')

out = []
seen = defaultdict(list)
for i, l in enumerate(LINES):
    m = re.match(r'^(#{1,4})\s+(.*)$', l)
    if m:
        seen[(len(m.group(1)), m.group(2).strip())].append(i + 1)
dups = {k: v for k, v in seen.items() if len(v) > 1}
out.append(u'=== 一、同層級同文標題重出：%d 組 ===' % len(dups))
for (lvl, t), v in sorted(dups.items(), key=lambda kv: kv[1][0]):
    out.append(u'  H%d ×%d｜%s｜L%s' % (lvl, len(v), t[:46], v[:6]))

# 二、款級標題之「序數＋首詞」重出（同節內易混者）
out.append('')
out.append(u'=== 二、各節之內 H4 序數重出（同號兩款）===')
cur = None
per = defaultdict(list)
order = []
for i, l in enumerate(LINES):
    if l.startswith('### ') and not l.startswith('####'):
        cur = (i + 1, l[4:].strip())
        order.append(cur)
        per[cur] = []
    elif l.startswith('#### ') and cur:
        m = re.match(u'^####\\s*(\\d{1,2}|[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]{1,3})\\s*、', l)
        if m:
            per[cur].append((m.group(1), i + 1, l[5:35]))
n = 0
for key in order:
    cnt = defaultdict(int)
    for a, ln, t in per[key]:
        cnt[a] += 1
    for a, c in cnt.items():
        if c > 1:
            n += 1
            out.append(u'  %s｜款號「%s」重出 %d 次' % (key[1][:26], a, c))
out.insert(2, u'（同節重出 %d 件）' % n)
open(os.path.join(HERE, 'duphead.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('dups', len(dups), 'reuse', n)
