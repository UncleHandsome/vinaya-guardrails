# -*- coding: utf-8 -*-
r"""longsite　列某章（或某附錄）印面長句之全文與行號（第 243 輪定名，源層工具）。

   用法：python _work/longsite.py 第四章 [閘值，預設 80]
   與第 52 軸 `r243long.py` 同一口徑（剔底冊、剔圍欄、剔表列與標題；列表項與引言塊俱收），
   差別只在本器把句子全文印出來供逐處落刀。口徑出處見附錄M 第 243 輪。
"""
import re, sys
sys.path.insert(0, '_work'); sys.path.insert(0, '.')
import _tk as t

want = sys.argv[1]
TH = int(sys.argv[2]) if len(sys.argv) > 2 else 80
L = t.LINES
BOT = t.bottom_lines()
CJK = re.compile(u'[一-鿿]')
FENCE = set()
run = False
for i in range(len(L)):
    if L[i].startswith(u'```'):
        run = not run
        FENCE.add(i)
        continue
    if run:
        FENCE.add(i)
CH, cur = {}, u'卷首'
for i, l in enumerate(L):
    m = re.match(u'^# (第[一二三四五六七八九]章|結語|終卷|附錄\\S+)', l)
    if m:
        cur = m.group(1)
    CH.setdefault(cur, []).append(i)
if want not in CH:
    print(u'無此篇：%s｜現有：%s' % (want, u' '.join(CH)))
    sys.exit(1)
for i in CH[want]:
    if i in BOT or i in FENCE:
        continue
    s = L[i].strip()
    if not s or s[0] in u'#|':
        continue
    body = re.sub(u'^([*\\-] |\\d+\\. )+', u'', s)
    for seg in re.split(u'[。；！？]', body):
        n = len(CJK.findall(seg))
        if n > TH:
            print(u'=== L%-6d %3d 字｜%s\n' % (i + 1, n, seg.strip()))
