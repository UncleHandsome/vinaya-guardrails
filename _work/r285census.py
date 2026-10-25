# -*- coding: utf-8 -*-
import io, os, re

KEY = [u'候裁', u'待裁', u'待作者', u'親裁', u'未裁', u'候令', u'候親裁', u'未奉令', u'不代筆']
SRC = [(u'_archive/編年工程日誌.md', 780, 952),
       (u'列印SOP.md', 1, 10 ** 6)]
MEMDIR = os.path.expanduser(u'~/.qoder/projects/C--Users-lionc-OneDrive-----------------/memory')
OUT = []
tot = 0
for p, a, b in SRC:
    L = io.open(p, encoding=u'utf-8').read().split(u'\n')
    for i in range(a - 1, min(b, len(L))):
        l = L[i]
        for m in re.finditer(u'|'.join(KEY), l):
            tot += 1
            s = max(0, m.start() - 160)
            OUT.append(u'%s:%d ▸ …%s…' % (p, i + 1, l[s:m.end() + 200].replace(u'\n', u'')))
for fn in sorted(os.listdir(MEMDIR)):
    if not fn.endswith(u'.md'):
        continue
    L = io.open(os.path.join(MEMDIR, fn), encoding=u'utf-8').read().split(u'\n')
    for i, l in enumerate(L):
        for m in re.finditer(u'|'.join(KEY), l):
            tot += 1
            s = max(0, m.start() - 160)
            OUT.append(u'memory/%s:%d ▸ …%s…' % (fn, i + 1, l[s:m.end() + 200].replace(u'\n', u'')))
io.open(u'_work/r285census.txt', 'w', encoding=u'utf-8', newline=u'\n').write(
    u'\n\n'.join(OUT))
print(u'命中 %d 處・摘片 %d 段・檔 %d 字' % (tot, len(OUT), sum(len(o) for o in OUT)))
