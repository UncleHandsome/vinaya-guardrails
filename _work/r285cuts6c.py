# -*- coding: utf-8 -*-
"""285・批六丙：#60 續——目錄尚存五條長題（9.4〜10.0pt），一律主題精簡・副題落正文。
   用法：python -X utf8 _work/r285cuts6c.py [--apply]"""
import io
import sys
import unicodedata

P = u'ver39四分律_起心動念心智分析框架_修正版.md'
APPLY = u'--apply' in sys.argv
S = io.open(P, encoding=u'utf-8').read()
NL = u'\r\n' if u'\r\n' in S else u'\n'
T = S.replace(u'\r\n', u'\n')
LOG = []


def w(s):
    return sum(2 if unicodedata.east_asian_width(c) in u'WF' else 1 for c in s)


def rep(old, new, label):
    global T
    c = T.count(old)
    assert c == 1, u'【%s】命中 %d 見・期 1' % (label, c)
    oh = old.split(u'\n')[0]
    nh = new.split(u'\n')[0]
    LOG.append(u'%-16s 題寬 %d➔%d' % (label, w(oh), w(nh)))
    assert w(nh) <= 68, u'【%s】新題仍寬 %d' % (label, w(nh))
    T = T.replace(old, new, 1)


rep(u'### 【經典地標深描 03】迦留陀夷七度試探——欲望從肢體試探到「持戒第一」神聖索供的微觀換裝\n',
    u'### 【經典地標深描 03】迦留陀夷七度試探——從肢體試探到神聖索供\n\n'
    u'本案之題旨在：欲望如何自**肢體之試探**換裝為**『持戒第一』之神聖索供**——微觀換裝之全軌。'
    u'此其副題，正文一依此判。\n', u'地標 03')
rep(u'### 【雙螺旋對照專題 03】年少比丘隔晨自首 vs 隱匿覆藏跨越明相——生路與代價的心理學對沖律\n',
    u'### 【雙螺旋對照專題 03】隔晨自首 vs 跨越明相——生路與代價之對沖\n\n'
    u'本組之題旨在：**年少比丘隔晨自首**之最高寬免，對照**隱匿覆藏跨越明相**之逐日代價——'
    u'同一明相，一生路一死結，是其心理學之對沖律。此其副題，正文一依此判。\n', u'雙螺旋 03')
rep(u'### 【經典地標深描 06】以錢易錢與棄金銀羯磨——出家人涉足金融炒作的銅臭之恥與淨人體制\n',
    u'### 【經典地標深描 06】以錢易錢與棄金銀——涉足金融之恥與淨人體制\n\n'
    u'本案之題旨在：出家人涉足**金融炒作**之銅臭，與僧團以**棄金銀羯磨**立淨人・守園人之體制。'
    u'此其副題，正文一依此判。\n', u'地標 06')
rep(u'### 【雙螺旋對照專題 04】借生薑易熱飯 vs 金布祇園名位相讓——對價商貿與功德奉獻的資產分水嶺\n',
    u'### 【雙螺旋對照專題 04】借薑易飯 vs 金布布地——對價與奉獻之分水嶺\n\n'
    u'本組之題旨在：**以生薑易熱飯**之對價商貿，對照**金錢側布滿地**之功德奉獻——'
    u'同一手持物，一成販賣一成供養，是其資產之分水嶺。此其副題，正文一依此判。\n', u'雙螺旋 04')
rep(u'### 【雙螺旋對照專題 05】慇懃勸足食 vs 泉水停供反被舉——偽善設局與特權反咬的瞋恚變臉\n',
    u'### 【雙螺旋對照專題 05】勸足食 vs 停供被舉——偽善設局與特權反咬\n\n'
    u'本組之題旨在：**慇懃勸與足食**之偽善設局，對照**泉水停供反被舉**之特權反咬——'
    u'同出一瞋恚，兩副變臉。此其副題，正文一依此判。\n', u'雙螺旋 05')

print(u'\n'.join(LOG))
print(u'行數 %+d' % (len(T.split(u'\n')) - len(S.split(u'\n'))))
if APPLY:
    io.open(u'_archive/備份/ver39.pre285k.md', 'w', encoding=u'utf-8', newline=u'\n').write(S)
    io.open(P, 'w', encoding=u'utf-8', newline=NL).write(T)
    print(u'已寫入')
else:
    print(u'（試跑・未寫檔）')
