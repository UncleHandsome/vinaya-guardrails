# -*- coding: utf-8 -*-
"""第六十七輪探測：其一、全書表格欄數完整性（表頭╱對齊列╱資料列）；
其二、書中「第N章第N節」式指涉之內容性核對（該節實為何物）。"""
import io
import re
from collections import defaultdict

import _tk as t

L = io.open(t.SRC, encoding='utf-8').read().split('\n')
out = []

# ── 一、表格欄數完整性 ──
def ncols(line):
    c = line.split('|')
    if c and not c[0].strip():
        c = c[1:]
    if c and not c[-1].strip():
        c = c[:-1]
    return len(c)

blocks = []
i = 0
while i < len(L):
    if L[i].lstrip().startswith('|') and i + 1 < len(L) and re.match(r'^\s*\|[\s:|-]+\|\s*$', L[i + 1]):
        j = i
        rows = []
        while j < len(L) and L[j].lstrip().startswith('|'):
            rows.append(j + 1)
            j += 1
        blocks.append((i + 1, rows))
        i = j
    else:
        i += 1

out.append('=== 一、表格 %d 面：欄數不一致者 ===' % len(blocks))
bad = []
for start, rows in blocks:
    n0 = ncols(L[rows[0] - 1])
    if ncols(L[rows[1] - 1]) != n0:
        bad.append((rows[0], '對齊列', ncols(L[rows[1] - 1]), n0))
    for r in rows[2:]:
        if ncols(L[r - 1]) != n0:
            bad.append((r, '資料列', ncols(L[r - 1]), n0))
for r, kind, got, want in bad:
    out.append('L%-6d %s 欄 %d != 表頭 %d | %s' % (r, kind, got, want, L[r - 1][:90]))
out.insert(1, '不一致 %d 列' % len(bad))

# ── 二、「第N章第N節」式指涉之內容核對：建節目的表 ──
h1 = None
sec_of = defaultdict(dict)   # 章 -> {節序: 節題}
CN = u'一二三四五六七八九十'
cur = None
for i, l in enumerate(L):
    m = re.match(r'^# (第[..]章)', l[:12])
    if l.startswith('# '):
        mm = re.match(r'^# (第(.)章)', l)
        if mm:
            cur = mm.group(2)
            h1 = l[2:20]
        else:
            cur = re.sub(r'[^A-Z]', '', l[:8]) or None
    if cur and l.startswith('### '):
        m3 = re.match(r'^### 第(.)節', l)
        if m3:
            sec_of[cur][m3.group(1)] = l[4:44]

out.append('')
out.append('=== 二、書中「第N章第M節」指涉 ↔ 該節實際節題（抽驗：指涉句與節題有無 keyword 相通）===')
pat = re.compile(u'第([一二三四五六七八九])章第([一二三四五六七八九十])節')
seen = defaultdict(int)
lines_hit = []
for i, l in enumerate(L):
    for m in pat.finditer(l):
        a, b = m.group(1), m.group(2)
        title = sec_of.get(a, {}).get(b[0] if len(b) > 1 else b)
        key = (a, b)
        seen[key] += 1
        lines_hit.append((i + 1, a, b, title, l[:80]))
out.append('指涉總計 %d 筆；節次對照：' % len(lines_hit))
for (a, b), n in sorted(seen.items(), key=lambda kv: -kv[1]):
    out.append('  第%s章第%s節 = 「%s」：%d 見' % (a, b, sec_of.get(a, {}).get(b, '【節序不存在】'), n))
missing = [x for x in lines_hit if x[3] is None]
out.append('')
out.append('指向不存在節序者 %d 筆' % len(missing))
for n, a, b, ti, ctx in missing[:20]:
    out.append('  L%d 第%s章第%s節 | %s' % (n, a, b, ctx))
io.open('_work/sweep67.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written', len(out), 'bad rows', len(bad))
