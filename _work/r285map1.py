# -*- coding: utf-8 -*-
"""285・結構總量（一）：章階・目錄・附錄・欄題・雙螺旋・凡例——只印行號與短摘。"""
import io
import re

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
L = io.open(P, encoding=u'utf-8').read().replace(u'\r\n', u'\n').split(u'\n')
OUT = []


def w(s):
    OUT.append(s)


def hd(startswith, pat=None):
    return [(i + 1, x) for i, x in enumerate(L)
            if x.startswith(startswith) and (pat is None or re.search(pat, x))]


w(u'◆ 全部 H1（%d 條）' % len(hd(u'# ')))
for i, x in hd(u'# '):
    w(u'  L%-5d %s' % (i, x[:60]))

w(u'\n◆ 第七章・第八章之 H2／H3（章內層級）')
h1 = [i for i, x in enumerate(L) if x.startswith(u'# 第七章') or x.startswith(u'# 第八章')]
ends = []
for i in h1:
    j = next((k for k in range(i + 1, len(L)) if L[k].startswith(u'# ')), len(L))
    ends.append(j)
for a, b in zip(h1, ends):
    w(u'  章 L%d〜L%d（%d 行）' % (a + 1, b, b - a))
    for k in range(a, b):
        if L[k].startswith(u'## ') or L[k].startswith(u'### '):
            w(u'    L%-5d %s' % (k + 1, L[k][:58]))

w(u'\n◆ 卷首目錄・第七／八章與附錄六之條目行')
T0 = next(i for i, x in enumerate(L) if x.startswith(u'# 第六章'))
for i in range(0, T0):
    x = L[i]
    if re.match(u'^\\s*[-*] ', x) and (u'第七章' in x or u'第八章' in x or u'附錄六' in x or u'終卷' in x):
        w(u'  L%-5d %s' % (i + 1, x[:120]))

w(u'\n◆ 全書『補遺 NN』與〔調部深描』之落點')
for i, x in enumerate(L):
    if re.search(u'補遺', x) or u'調部深描' in x:
        w(u'  L%-5d %s' % (i + 1, x[:110]))

w(u'\n◆ 第六章 14 處『律典原典逐字回查』H4・及其下之段樣')
for i, x in enumerate(L):
    if x.startswith(u'####') and u'原典' in x and u'回查' in x:
        seg = [y for y in L[i + 1:i + 14] if y.strip()][:3]
        w(u'  L%-5d %s' % (i + 1, x[:44]))
        for s in seg:
            w(u'        ▸ %s' % s[:96])

w(u'\n◆ 雙螺旋 01〜06 之題與欄結構')
for i, x in enumerate(L):
    if x.startswith(u'####') and u'螺旋' in x:
        w(u'  L%-5d %s' % (i + 1, x[:64]))
        for k in range(i + 1, min(i + 40, len(L))):
            if L[k].startswith(u'####'):
                break
            if L[k].startswith(u'#####') or (L[k].startswith(u'**') and u'：**' in L[k][:14]):
                w(u'        %s| %s' % (k + 1, L[k][:52]))

w(u'\n◆ 凡例・第二節三層標記／原典層／十四欄 三處全文')
for i in range(0, 300):
    if u'三層標記' in L[i] or u'今十四欄' in L[i] or u'原典層' in L[i]:
        w(u'  L%-5d %s' % (i + 1, L[i][:300]))

w(u'\n◆ 附錄三・附錄五前言・檢核表第十四項・判準層級表・臨濟四奪・求聽第一階')
KEY = [(u'附錄五', 3), (u'檢核表', 2), (u'判準層級', 3), (u'人境兩俱奪', 2),
       (u'從彼求聽', 4), (u'阿難', 2), (u'五遍行', 3), (u'不忍', 4),
       (u'截圖', 3), (u'備案', 3), (u'小參', 3), (u'視訊會議', 2), (u'數位資產', 2),
       (u'長照', 2), (u'寺產借名代持', 2), (u'自始無受樂', 1), (u'不可反駁推定', 1)]
for k, lim in KEY:
    got = [(i + 1, x) for i, x in enumerate(L) if k in x]
    w(u'  【%s】%d 見' % (k, len(got)))
    for i, x in got[:lim]:
        w(u'      L%-5d %s' % (i, x[:100]))

io.open(u'_work/r285map1.txt', 'w', encoding=u'utf-8', newline=u'\n').write(u'\n'.join(OUT))
w2 = sum(len(o) for o in OUT)
print(u'印出 %d 段・%d 字 ➔ _work/r285map1.txt' % (len(OUT), w2))
