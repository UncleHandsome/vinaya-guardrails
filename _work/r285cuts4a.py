# -*- coding: utf-8 -*-
"""285・批四甲：#39 雙螺旋 02〜06 各補『律典原典逐字回查』一欄（逐字俱自附錄四該案之cell複製，不重打）
   ＋兩處『今十四欄』➔『今十九欄』。用法：python -X utf8 _work/r285cuts4a.py [--apply]"""
import io
import re
import sys

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
T = S.replace(u'\r\n', u'\n')
L = T.split(u'\n')

A4 = next(i for i, x in enumerate(L) if x.startswith(u'# 附錄四'))
A5 = next(i for i, x in enumerate(L) if x.startswith(u'# 附錄五'))
CELL = {}
for i in range(A4, A5):
    m = re.match(u'^\\| \\*\\*〔案例 (\\d+)〕[^|]*\\|([^|]*)\\|(.*)$', L[i])
    if m:
        vol, body = m.group(2).strip(), m.group(3)
        quotes = re.findall(u'「[^」]*」', body)
        if quotes:
            CELL[int(m.group(1))] = (vol, quotes)
print(u'附錄四可取之案 %d 個' % len(CELL))

GROUPS = {2: (10, 11), 3: (25, 57), 4: (29, 97), 5: (49, 98), 6: (93, 84)}
SPECIAL = {25: u'卷次未細核（文在本地三十八至四十九卷分段檔·僧殘治法羯磨之段）'}
HDR = u'> **《四分律》%s·大正藏 No. 1428**  '
for g, cases in GROUPS.items():
    for n in cases:
        assert n in CELL, u'案 %d 在附錄四無逐字可複製' % n

blocks = {}
for g, cases in GROUPS.items():
    out = [u'#### 律典原典逐字回查', u'']
    for n in cases:
        vol, quotes = CELL[n]
        if n in SPECIAL:
            disp = SPECIAL[n]
        else:
            parts = vol.split(u'·')
            disp = parts[0] + (u'（%s）' % u'·'.join(parts[1:]) if len(parts) > 1 else u'')
        out.append(HDR % disp)
        for q in quotes:
            out.append(u'> ' + q)
        out.append(u'')
    while out and out[-1] == u'':
        out.pop()
    blocks[g] = out
    print(u'組 0%d：卷段 %s・引段 %d・%d 行' % (
        g, u'／'.join(CELL[n][0] for n in cases),
        sum(len(CELL[n][1]) for n in cases), len(out)))

INS = []
for g, cases in GROUPS.items():
    t = next(i for i, x in enumerate(L) if x.startswith(u'### 【雙螺旋對照專題 0%d】' % g))
    h = next(i for i in range(t + 1, len(L))
             if re.match(u'^#{1,3} ', L[i]) and not L[i].startswith(u'####'))
    rule = next(i for i in range(h - 1, t, -1) if L[i] == u'---')
    INS.append((rule, blocks[g], g))
    print(u'  插點 0%d ➔ L%d（%-5s 之前）' % (g, rule + 1, L[h][:12]))

NEW = list(L)
for rule, blk, g in sorted(INS, reverse=True):
    NEW[rule + 1:rule + 1] = [u''] + blk + [u'', u'---']
T2 = u'\n'.join(NEW)

# 兩處欄數之自稱
OLD1 = u'（今十四欄，一欄可覆數案，非一案一欄）'
T2n1 = T2.count(OLD1)
assert T2n1 == 1, u'凡例之十四欄錨非一：%d' % T2n1
T2 = T2.replace(OLD1, u'（今十九欄，一欄可覆數案，非一案一欄）')
OLD2 = (u'一、十三則地標各附『律典原典逐字回查』一欄，雙螺旋唯 01 附之（全書今十四欄，與凡例之數合）；'
        u'02〜06 之原典俱已匯入附錄四各案之卡，此處不復重貼——速查與深描之責有分，逐字之責在附錄四。')
assert T2.count(OLD2) == 1, u'卷首括注之錨非一'
T2 = T2.replace(OLD2, u'一、十三則地標與六組雙螺旋各附『律典原典逐字回查』一欄（全書今十九欄，與凡例之數合）；'
                      u'欄中所錄唯結戒與判語之原文，事相與處斷之詳仍各在其地標・速查與附錄四——'
                      u'速查與深描之責有分，逐字之責在欄與附錄四。')
cnt = len(re.findall(u'(?m)^#### (?:五、)?律典原典逐字回查$', T2))
print(u'校：欄今 %d（期 19）・行數 %+d' % (cnt, len(T2.split(u'\n')) - len(L)))
assert cnt == 19, u'欄數非 19'
assert u'今十四欄' not in T2

if APPLY:
    io.open(u'_archive/備份/ver39.pre285e.md', 'w', encoding=u'utf-8', newline=u'\n').write(T)
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T2)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
