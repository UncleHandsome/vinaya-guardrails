# -*- coding: utf-8 -*-
"""第五章心所總表 ↔ 《成唯識論》本文之內容覆核：六位之數與各組名單。"""
import io, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _tk

ROOT, norm = _tk.ROOT, _tk.norm
TXT = u''.join(io.open(f, encoding='utf-8-sig').read() for f in sorted(glob.glob(os.path.join(ROOT, u'佛經', u'成唯識論', u'*.txt'))))
NT = norm(TXT)
L = _tk.LINES

rows = {}
for i in range(1048, 1058):
    if L[i].startswith(u'|'):
        c = [x.strip() for x in L[i].strip(u'|').split(u'|')]
        if len(c) >= 3 and c[1].isdigit():
            rows[c[0].strip('*')] = (int(c[1]), [x.strip() for x in re.split(u'、', re.sub(u'（[^）]*）', u'', c[2]))])

out = [u'書中總表：%s' % u'；'.join(u'%s=%d(%d名)' % (k, v[0], len(v[1])) for k, v in rows.items())]
tot = sum(len(v[1]) for v in rows.values())
out.append(u'名數合計 %d；宣稱合計 %d' % (tot, sum(v[0] for v in rows.values())))
miss = []
for k, (n, names) in rows.items():
    for nm in names:
        if not nm:
            continue
        if norm(nm) not in NT:
            miss.append(u'%s/%s' % (k, nm))
out.append(u'《成唯識論》本文查無其形者 %d 名：%s' % (len(miss), u'、'.join(miss) or u'無'))
for pat in (u'遍行有五', u'別境有五', u'善十一', u'煩惱有六', u'隨煩惱二十', u'不定有四',
            u'初遍行別境', u'五三一二六十有四種'):
    out.append(u'[%s] 論中%s' % (pat, u'見' if norm(pat) in NT else u'0 見'))
io.open(os.path.join(ROOT, u'_work', u'xschk.txt'), 'w', encoding=u'utf-8').write(u'\n'.join(out))
print(tot, len(miss))
