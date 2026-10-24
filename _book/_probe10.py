# -*- coding: utf-8 -*-
"""〔案：〕諸記之細量：所在之區、落點、上下文、其性質。"""
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
APX = next(i for i, l in enumerate(L, 1) if l.startswith(u'# 【卷末'))
FIRST = next(i for i, l in enumerate(L, 1) if l.startswith(u'# 第') and u'章' in l)
NOTE = re.compile(u'〔案：([^〕]{4,400})〕')

def heads_upto(n):
    ch = sec = cs = u'？'
    for i, l in enumerate(L, 1):
        if i > n:
            break
        if l.startswith(u'# '):
            ch, sec, cs = l[2:14], u'？', u'？'
        elif l.startswith(u'## '):
            sec, cs = l[3:24], u'？'
        elif l.startswith(u'### '):
            cs = l[4:26]
    return ch, sec, cs

rows = []
for i, l in enumerate(L, 1):
    for m in NOTE.finditer(l):
        zone = u'卷首' if i < FIRST else (u'正文' if i < APX else u'附錄')
        txt = m.group(1)
        pre = l[max(0, m.start() - 46):m.start()].replace(u'\n', u' ')
        rows.append((i, zone, heads_upto(i), txt, pre))
print(u'共 %d 條｜卷首 %d・正文 %d・附錄 %d' % (
    len(rows), len([r for r in rows if r[1] == u'卷首']),
    len([r for r in rows if r[1] == u'正文']), len([r for r in rows if r[1] == u'附錄'])))
for i, z, (ch, sec, cs), txt, pre in rows:
    print(u'\nL%-6d [%s] %s／%s／%s' % (i, z, ch, sec, cs))
    print(u'   前文…%s' % pre[-46:])
    print(u'   記｜%s（%d 字）' % (txt[:150], len(txt)))
