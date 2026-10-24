# -*- coding: utf-8 -*-
"""〔案：〕之分級：A＝記舊引之正（可遷附錄）；B＝護在位之實（須先降其式樣）；C＝附錄自用（留）。"""
import io, re

t = io.open(u'佛陀的護欄_四分律行為心理學與現代僧伽治理.md', encoding='utf-8').read()
L = t.split(u'\n')
APX = next(i for i, l in enumerate(L, 1) if l.startswith(u'# 【卷末'))
FIRST = next(i for i, l in enumerate(L, 1) if l.startswith(u'# 第') and u'章' in l)
NOTE = re.compile(u'〔案：([^〕]{4,400})〕')
B = re.compile(u'撮要|非逐字|今譯|本書之稱|乃本書|本書今?譯|編者依|類推|推演|姑標以存誠|方法學概括|白話|假設|補成|不稱逐字')
A = re.compile(u'舊引|律無|律之正判|全無|0 見|別無|律中查無')

def zone(i):
    return u'卷首' if i < FIRST else (u'正文' if i < APX else u'附錄')

def head(n):
    ch = cs = u'？'
    for i, l in enumerate(L, 1):
        if i > n:
            break
        if l.startswith(u'# '):
            ch, cs = l[2:12], u'？'
        elif l.startswith(u'### '):
            cs = l[4:24]
    return ch, cs

cnt = {}
for i, l in enumerate(L, 1):
    if zone(i) == u'附錄':
        continue
    for m in NOTE.finditer(l):
        txt = m.group(1)
        cls = u'B' if B.search(txt) else (u'A' if A.search(txt) else u'？')
        cnt.setdefault(zone(i) + cls, []).append((i, txt[:44]))
for k in sorted(cnt):
    print(u'%s ×%d' % (k, len(cnt[k])))
print(u'\n== 正文需降式樣者（B 與？）==')
for k in (u'正文B', u'正文？'):
    for i, x in cnt.get(k, []):
        ch, cs = head(i)
        print(u'  L%-6d %s｜%s｜%s' % (i, ch, cs[:22], x))
print(u'\n== 卷首者 ==')
for i, x in cnt.get(u'卷首A', []) + cnt.get(u'卷首B', []) + cnt.get(u'卷首？', []):
    print(u'  L%-6d %s' % (i, x))
