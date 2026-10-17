# -*- coding: utf-8 -*-
"""第七十四輪軸乙（定稿）：日本新字體／和製字形，加上 _tk 異體群首座形，掃其於引號外之出現。"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = [f for f in os.listdir(ROOT) if f.startswith('ver38') and f.endswith('.md')][0]
DOC = open(os.path.join(ROOT, MD), encoding='utf-8').read()
sys.path.insert(0, ROOT)
import _tk  # noqa

JP = list('関囲絵覚楽釈旧会着巻亜悪応桜労啓亀図専属沢済満滝灯炉鉄録')
SUS = set(JP) | set(g[0] for g in _tk.VARIANT_GROUPS)

spans = [m.span() for m in re.finditer('「[^」]*」|『[^』]*』', DOC)]


def inq(i):
    return any(a <= i < b for a, b in spans)


out = []
for ch in sorted(SUS):
    hits = [DOC[:i].count('\n') + 1 for i, c in enumerate(DOC) if c == ch and not inq(i)]
    allc = sum(1 for c in DOC if c == ch)
    if not allc:
        continue
    grp = [g for g in _tk.VARIANT_GROUPS if ch in g]
    out.append('  %s U+%04X 全%4d 引號外%4d %-26s 同群：%s'
               % (ch, ord(ch), allc, len(hits), str(hits[:5]), grp[0] if grp else '—'))
open(os.path.join(HERE, 'jp74.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('reported', len(out))
