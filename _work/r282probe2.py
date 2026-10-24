# -*- coding: utf-8 -*-
"""282・量（二）：外路第十一報告其餘九案之今檔現況。只讀不改。"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, u'ver39四分律_起心動念心智分析框架_修正版.md')
LINES = io.open(BOOK, encoding=u'utf-8-sig').read().split(u'\n')
T = u'\n'.join(LINES)


def show(title, needle, before=1, after=1, maxlen=160):
    print(u'==== %s [%s]' % (title, needle))
    for i, l in enumerate(LINES):
        if needle in l:
            for j in range(max(0, i - before), min(len(LINES), i + after + 1)):
                print(u'  L%d%s| %s' % (j + 1, u'►' if j == i else u' ', LINES[j][:maxlen]))
            print(u'  --')


# 甲・第七章第二節：同句重號與孤行
show(u'甲1 案例39 之全書載體', u'案例 39', 0, 0, 200)
show(u'甲2 案例67 之全書載體', u'案例 67', 0, 0, 200)

# 乙・附錄三人名表
i3 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄三'))
i4 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄四'))
print(u'==== 乙・附錄三 L%d..%d' % (i3 + 1, i4 + 1))
nam = [i for i in range(i3, i4) if u'人名' in LINES[i] and LINES[i].startswith(u'#')]
print(u'  人名小節：%s' % [(i + 1, LINES[i][:40]) for i in nam])
if nam:
    h = nam[0]
    end = next((i for i in range(h + 1, i4) if LINES[i].startswith(u'#')), i4)
    rows = [i for i in range(h, end) if LINES[i].lstrip().startswith(u'|')]
    print(u'  表列（含表頭分隔）：%d 行' % len(rows))
    for i in rows[:4] + rows[-3:]:
        print(u'  L%d| %s' % (i + 1, LINES[i][:120]))
    for who in [u'檀尼迦', u'沓婆', u'慈地', u'象力', u'檀那']:
        print(u'  %s 全書：%d・附錄三內：%d' % (who, T.count(who), sum(1 for i in rows if who in LINES[i])))
    for k in range(h, min(h + 14, end)):
        if LINES[k].strip() and not LINES[k].lstrip().startswith(u'|'):
            print(u'  文 L%d| %s' % (k + 1, LINES[k][:150]))

# 丙・附錄四 案例25／69 之卷宣稱
for n in (25, 69):
    pat = re.compile(u'〔案例 0*%d(?:[^0-9][^〕]*)?〕' % n)
    for i in range(i4, next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄五'))):
        if pat.search(LINES[i]):
            print(u'==== 丙・案%d L%d| %s' % (n, i + 1, LINES[i][:240]))

# 丁・第八章
i8 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 第八章'))
i9 = next((i for i, l in enumerate(LINES) if i > i8 and l.startswith(u'# ') and
           not l.startswith(u'# 第八章')), len(LINES))
print(u'==== 丁・第八章 L%d..%d' % (i8 + 1, i9 + 1))
for w in [u'當然解任', u'即刻', u'搜', u'票', u'假處分', u'登記', u'印鑑', u'止付', u'勞動']:
    hits = [i + 1 for i in range(i8, i9) if w in LINES[i]]
    print(u'  %-6s %d 處：%s' % (w, len(hits), hits[:12]))

# 戊・附錄六導言與調部
i6 = next(i for i, l in enumerate(LINES) if l.startswith(u'# 附錄六'))
print(u'==== 戊・附錄六起 L%d' % (i6 + 1))
for k in range(i6, i6 + 12):
    print(u'  L%d| %s' % (k + 1, LINES[k][:200]))
print(u'  『調部』全書：%d・附錄六內：%d' % (T.count(u'調部'),
      sum(LINES[i].count(u'調部') for i in range(i6, len(LINES)))))

# 己・壇經偈
for i, l in enumerate(LINES):
    if u'身來身去' in l or u'身去身來' in l:
        print(u'==== 己・壇經 L%d| %s' % (i + 1, l[:220]))
